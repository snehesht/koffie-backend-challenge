
dev:
	cd app && python3 -m uvicorn main:app --reload

start:
	@python3 app/main.py

test:
	@python3 -m pytest --asyncio-mode=strict