import aiosqlite

class VINResponse(dict):
	vin: str;
	make: str;
	model: str;
	model_year: str;
	body_class: str;
	cached_result: bool;

class CacheStore:
	def __init__(self, db_path):
		self.db_path = db_path
		self.db = None

	async def connect(self):
		self.db = await aiosqlite.connect(self.db_path)
		await self.db.execute('''
			CREATE TABLE IF NOT EXISTS cache (
				vin TEXT PRIMARY KEY NOT NULL,
				make TEXT NOT NULL,
				model TEXT NOT NULL,
				model_year TEXT NOT NULL,
				body_class TEXT NOT NULL,
				created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
			)
		''')
		await self.db.commit()

	async def close(self):
		await self.db.close()

	async def get_vin_data(self, vin: str) -> VINResponse | None: 
		"""
		Get the VIN data from the cache store, return None if the VIN is not found
		"""
		async with self.db.execute('SELECT * FROM cache WHERE vin = ?', (vin,)) as cursor:
			record = await cursor.fetchone()
			if (record != None):
				return VINResponse(
					vin=record[0],
					make=record[1],
					model=record[2],
					model_year=record[3],
					body_class=record[4],
					cached_result=True
				)
			return None;

	async def set_vin_data(self, vin: str, make: str, model: str, model_year: str, body_class: str) -> None:
		"""
		Store the VIN data in the cache store
		"""
		try:
			await self.db.execute('''
				INSERT INTO cache (vin, make, model, model_year, body_class)
				VALUES (?, ?, ?, ?, ?)
			''', (vin, make, model, model_year, body_class));
			await self.db.commit()
		except Exception as e:
			print('Error in writing vin ' + vin + ' data to cache store', e)
			raise e

	async def remove_vin_data(self, vin: str) -> bool:
		"""
		Remove a VIN from the cache store 
		Return true if the delete operation was successful, even if the VIN was not found in the cache store
		If the operation fails, return false
		"""
		try:
			await self.db.execute('''
				DELETE FROM cache WHERE vin = ?
			''', (vin,))
			await self.db.commit()
			return True
		except Exception as e:
			print('Error in removing vin ' + vin + ' data from cache store', e)
			return False


	async def export_vin_data(self) -> list:
		"""
		Export all the vehicle information from the cache store
		"""
		try:
			async with self.db.execute('SELECT vin, make, model, model_year, body_class FROM cache') as cursor:
				records = await cursor.fetchall()
				return records
		except Exception as e:
			print('Error in exporting vin data from cache store', e)
			raise e