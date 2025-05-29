#!/usr/bin/env python3
'''
Global Configuration for Project 'JobFluence'
'''

# config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ''' Global Base settings for web service
    '''
    # Maximum file size for resume uploads, in bytes (e.g., 5MB)
    MAX_FILE_SIZE: int = 5 * 1024 * 1024    #5 MB

    class Config:
        env_file = '.env.local'

settings = Settings()
