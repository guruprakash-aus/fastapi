start_db:
	docker compose -f ./db/docker-compose.yml -p fastapi_app up -d

stop_db:
	docker compose -p fastapi_app down