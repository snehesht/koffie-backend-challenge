from fastapi import FastAPI
from vpic.client import decode_vin

app = FastAPI()

@app.get('/health')
def health():
	return {'status': 'ok'}

@app.get("/")
async def read_index():
	response = await decode_vin('1XPWD40X1ED215307'); # 1G1Z3A1Z9C0390013
	return response

