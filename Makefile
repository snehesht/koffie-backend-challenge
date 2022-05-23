
dev:
	cd app && python3 -m uvicorn main:app --reload

start:
	@python3 app/main.py

test:
	@python3 -m pytest --asyncio-mode=strict
	
docker-build:
	@docker build -t koffie-background-challenge .

docker-run:
	@docker stop koffie-background-challenge || true
	@docker run -it -p 8000:8000 koffie-background-challenge:latest

docker: docker-build docker-run