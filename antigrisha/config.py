import os


class Config:
    OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
    FOLDER_ID = os.getenv('FOLDER_ID')

    API_ID = os.getenv('API_ID')
    API_HASH = os.getenv('API_HASH')
