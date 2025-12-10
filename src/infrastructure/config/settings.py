import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_MAPS_API_KEY: str
    DEFAULT_RADIUS: int = 3000
    DEFAULT_MAX_RESULTS: int = 60


    class Config:
        '''Configuration for environment variables
        Attributes:
            env_file (str): Path to the .env file
            env_file_encoding (str): Encoding of the .env file
            Google Maps API key
            Default search radius in meters
            Default maximum number of results to fetch
        '''
        GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
        if not GOOGLE_MAPS_API_KEY:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set.")
        DEFAULT_RADIUS = 3000
        DEFAULT_MAX_RESULTS = 60
        
        env_file = ".env"
        env_file_encoding = "utf-8"
        
