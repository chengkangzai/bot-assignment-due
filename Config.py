from dotenv import dotenv_values
import os


class Config:
    def __init__(self):
        env = dotenv_values(".env")
        self.APP_DEBUG = os.environ.get("APP_DEBUG", env.get("APP_DEBUG", True))
        self.APP_DEBUG = os.environ.get("APP_ENV", env.get("APP_ENV", "production"))

        self.DB_HOST = os.environ.get("DB_HOST", env.get('DB_HOST', '127.0.0.1'))
        self.DB_PORT = os.environ.get("DB_PORT", env.get('DB_PORT', '3306'))
        self.DB_DATABASE = os.environ.get("DB_DATABASE", env.get('DB_DATABASE', 'db'))
        self.DB_USERNAME = os.environ.get("DB_USERNAME", env.get('DB_USERNAME', 'root'))
        self.DB_PASSWORD = os.environ.get("DB_PASSWORD", env.get('DB_PASSWORD', ''))

        self.DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", env.get("DISCORD_TOKEN"))
        self.COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", env.get("COMMAND_PREFIX"))
