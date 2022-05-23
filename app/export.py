import pandas as pd
import tempfile
from uuid import uuid4
from fastparquet import write
from store import CacheStore
from logger import logger

async def export_cache(store: CacheStore):
	"""
	Export all the vehicle information from the cache store in parquet format
	"""
	try:
		temp_parquet_file = tempfile.gettempdir() + '/' + str(uuid4()) + '.parquet';
		data = await store.export_vin_data()
		df = pd.DataFrame(data, columns=['vin', 'make', 'model', 'model_year', 'body_class'])
		logger.info("Writing parquet file to: " + temp_parquet_file)
		write(temp_parquet_file, df)
		return temp_parquet_file
	except Exception as e:
		logger.critical('Error exporting cache to parquet file format', e)
		raise e