import uvicorn
from fastapi import FastAPI, Path, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os
import datetime
from vpic.client import decode_vin
from store import CacheStore, VINResponse
from export import export_cache

app = FastAPI()

store = CacheStore('store.db')

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

# Health Check to ensure the server is running
@app.get('/health')
def health():
	return {'status': 'ok', 'timestamp': datetime.datetime.now().timestamp()}


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
		print('Error looking up VIN: ', e)
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
		print('Error: ', e)
		return {'cache_delete_success': False, 'vin': vin}


@app.post("/export", response_class=FileResponse)
async def export(background_tasks: BackgroundTasks):
	"""
	Export all the vehicle information from the cache store in parquet format
	"""
	temp_parquest_file_path = ""
	try:
		temp_parquest_file_path = await export_cache(store)
		return temp_parquest_file_path
	except Exception as e:
		print('Error: ', e)
		raise HTTPException(status_code=422, detail=str(e))
	finally:
		# Remove the temporary parquet file
		if (temp_parquest_file_path != ""):
			background_tasks.add_task(os.remove, temp_parquest_file_path);


# Entry point
if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1')