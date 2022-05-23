import httpx 
import logging
from typing import TypedDict

logger = logging.getLogger(__name__)
class VehicleInfo(TypedDict):
	vin: str
	make: str
	model: str
	modle_year: str
	body_class: str

async def decode_vin(vin: str) -> VehicleInfo:
	"""
	Decode a VIN with vPIC API.
	Reference: https://vpic.nhtsa.dot.gov/api
	"""
	try:
		url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/' + vin + '?format=json'
		async with httpx.AsyncClient() as client:
			response = await client.get(url)
			data = response.json()

			# Check if vPIC API returned results
			if (len(data["Results"]) == 0):
				raise Exception("No data found for VIN: " + str(vin))

			# Get the first result
			vin_data = data["Results"][0]; 

			# If VIN is not decoded, ErrorCode will not be 0
			error_code = vin_data["ErrorCode"];
			if (error_code != "0"):
				raise Exception("Error: " + vin_data["ErrorText"])
			
			return VehicleInfo(
				vin=vin_data["VIN"], 
				make=vin_data["Make"],
				model=vin_data["Model"],
				model_year=vin_data["ModelYear"],
				body_class=vin_data["BodyClass"]
			);
	except Exception as e:
		logger.critical("Error decoding VIN: " + vin + " with vPIC API", e)
		raise e