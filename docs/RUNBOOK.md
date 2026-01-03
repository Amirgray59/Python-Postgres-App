docker compose exec api alembic upgrade head


docker compose exec api alembic revision --autogenerate -m "create users items tags"


docker compose exec api alembic downgrade base


docker compose exec api python app/scripts/clean_mongo.py


