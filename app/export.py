import pandas as pd
import tempfile
from uuid import uuid4
from fastparquet import write
from store import CacheStore

async def export_cache(store: CacheStore):
	"""
	Export all the vehicle information from the cache store in parquet format
	"""
	try:
		temp_parquet_file = tempfile.gettempdir() + '/parq/' + str(uuid4()) + '.parquet';
		data = await store.export_vin_data()
		df = pd.DataFrame(data, columns=['vin', 'make', 'model', 'model_year', 'body_class'])
		write(temp_parquet_file, df)
		return temp_parquet_file
	except Exception as e:
		print('Error exporting cache to parquet file format', e)
		raise e