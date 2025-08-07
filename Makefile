# start_db:
# 	docker compose -f ./db/docker-compose.yml -p fastapi_app up -d

# stop_db:
# 	docker compose -p fastapi_app down

start_prod_api:
	docker compose -f ./docker-compose-prod.yml -p fastapi_app up -d

stop_prod_api:
	docker compose -f ./docker-compose-prod.yml -p fastapi_app down

start_dev_api:
	docker compose -f ./docker-compose-dev.yml -p fastapi_app up -d

stop_dev_api:
	docker compose -f ./docker-compose-dev.yml -p fastapi_app down
