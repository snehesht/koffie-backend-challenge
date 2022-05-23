import uvicorn
from fastapi import FastAPI, Path, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, RedirectResponse
import os
import datetime
from vpic.client import decode_vin
from store import CacheStore, VINResponse
from export import export_cache
from logger import logger

# Database file path
# When running on stateless environments, use presisted volume path to store the database
db_file = os.path.join(os.path.dirname(__file__), 'store.db')

app = FastAPI()

store = CacheStore(db_file)

# Startup Workflow
@app.on_event("startup")
async def startup_event():
	# Connect to the database
	await store.connect();

# Shutdown Workflow
@app.on_event("shutdown")
async def shutdown_event():
	# Close the database connection
	await store.close();

@app.get('/health')
def health():
	"""
	Health Check to check if the app is running. Required when deploying in Kubernetes or other environments
	"""
	return {'status': 'ok', 'timestamp': datetime.datetime.now().timestamp()}


@app.get('/')
def index():
	"""
	Redirect Index to the Swagger UI
	"""
	return RedirectResponse("/docs")

# API Endpoints
@app.get("/lookup/{vin}")
async def lookup(
	vin: str = Path(title="VIN", description="Vehicle Identification Number", regex="^[A-Z0-9]{17}$"),
):
	"""
	Lookup vehicle information by VIN
	"""
	try:
		cached_data = await store.get_vin_data(vin) # 1XPWD40X1ED215307
		if (cached_data != None):
			return cached_data;
		
		# Lookup data from vPIC API
		data = await decode_vin(vin); # 1G1Z3A1Z9C0390013

		# Save the data to the cache store
		await store.set_vin_data(
			vin = data['vin'], 
			make = data['make'], 
			model = data['model'], 
			model_year = data['model_year'], 
			body_class = data['body_class'])

		# Return VIN data
		return VINResponse(
			vin=data['vin'],
			make=data['make'],
			model=data['model'],
			model_year=data['model_year'],
			body_class=data['body_class'],
			cached_result=False
		);
	except Exception as e:
		logger.critical('Error looking up VIN', e)
		raise HTTPException(status_code=400, detail=str(e))


@app.delete("/remove/{vin}")
async def remove(
	vin: str = Path(title="VIN", description="Vehicle Identification Number", regex="^[A-Z0-9]{17}$"),
):
	"""
	Remove vehicle information by VIN
	"""
	try:
		status = await store.remove_vin_data(vin)
		return {'cache_delete_success': status, 'vin': vin}
	except Exception as e:
		logger.critical('Error removing VIN from cache', e)
		return {'cache_delete_success': False, 'vin': vin}


@app.post("/export", response_class=FileResponse)
async def export(background_tasks: BackgroundTasks):
	"""
	Export all the data from the cache store in parquet format
	"""
	temp_parquest_file_path = ""
	try:
		temp_parquest_file_path = await export_cache(store)
		return temp_parquest_file_path
	except Exception as e:
		logger.critical('Error exporting cache to parquet file format', e)
		raise HTTPException(status_code=422, detail=str(e))
	finally:
		# Remove the temporary parquet file using background tasks to 
		# ensure it is removed after the response is sent
		if (temp_parquest_file_path != ""):
			background_tasks.add_task(os.remove, temp_parquest_file_path);


# Entry point
if __name__ == '__main__':
	logger.info('Starting VIN Cache Service');
	uvicorn.run("main:app", port=8000, host='0.0.0.0', log_level="critical");