
dev:
	cd app && python3 -m uvicorn main:app --reload

test:
	@python3 -m pytest --asyncio-mode=strict