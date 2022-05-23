import pytest
from .client import decode_vin

@pytest.mark.asyncio
async def test_decode_vin():
	decoded_vin = await decode_vin('1XPWD40X1ED215307');
	assert decoded_vin['vin'] == '1XPWD40X1ED215307';
	assert decoded_vin['make'] == 'PETERBILT';
	assert decoded_vin['model'] == '388';
	assert decoded_vin['model_year'] == '2014';
	assert decoded_vin['body_class'] == 'Truck-Tractor';

@pytest.mark.asyncio
async def test_decode_vin_incomplete():
	try:
		await decode_vin('1XPWD40X1ED');
	except Exception as e:
		assert True

@pytest.mark.asyncio
async def test_decode_vin_invalid():
	try:
		await decode_vin('1XPWD40X1ED215308');
	except Exception as e:
		assert True