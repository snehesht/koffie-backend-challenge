import pytest
from .client import decode_vin

@pytest.mark.asyncio
async def test_decode_vin():
	decoded_vin = await decode_vin('1XPWD40X1ED215307');
	assert decoded_vin['vin'] == '1XPWD40X1ED215307';
	assert decoded_vin['make'] == 'PETERBILT';
	assert decoded_vin['model'] == '388';
	assert decoded_vin['modle_year'] == '2014';
	assert decoded_vin['body_class'] == 'Truck-Tractor';

@pytest.mark.asyncio
async def test_decode_vin_incomplete():
	with pytest.raises(Exception) as excinfo:
		await decode_vin('1XPWD40X1ED');
	assert 'Error: 6 - Incomplete VIN' in str(excinfo.value)