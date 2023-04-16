from pydantic import BaseSettings

class Settings(BaseSettings):
    #List all env variables
    database_hostname: str 
    database_port: str
    database_password: str 
    database_name: str
    database_username: str  
    # for JSON web tokens
    secret_key: str 
    # for signing token
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file =".env"

settings = Settings()