from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5422"
    database_name: str = "postgres_db"
    database_username: str = "user"
    database_password: str = "password"
    secret_key: str = "your_secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
