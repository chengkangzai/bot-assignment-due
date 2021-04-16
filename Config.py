from dotenv import dotenv_values
import os


class Config:
    def __init__(self):
        env = dotenv_values(".env.local")
        self.APP_DEBUG = os.environ.get("APP_DEBUG", env.get("APP_DEBUG", True))
        self.APP_ENV = os.environ.get("APP_ENV", env.get("APP_ENV", "production"))

        self.DB_HOST = os.environ.get("DB_HOST", env.get('DB_HOST', '127.0.0.1'))
        self.DB_PORT = os.environ.get("DB_PORT", env.get('DB_PORT', '3306'))
        self.DB_DATABASE = os.environ.get("DB_DATABASE", env.get('DB_DATABASE', 'db'))
        self.DB_USERNAME = os.environ.get("DB_USERNAME", env.get('DB_USERNAME', 'root'))
        self.DB_PASSWORD = os.environ.get("DB_PASSWORD", env.get('DB_PASSWORD', ''))

        self.DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", env.get("DISCORD_TOKEN"))
        self.COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", env.get("COMMAND_PREFIX"))


if __name__ == "__main__":
    print('1. Print All the Config')
    operation = input("What you want")
    if operation == "1":
        print(f"""
APP_DEBUG       = {Config().APP_DEBUG} 
APP_ENV         = {Config().APP_ENV} 
DB_HOST         = {Config().DB_HOST} 
DB_PORT         = {Config().DB_PORT} 
DB_DATABASE     = {Config().DB_DATABASE} 
DB_USERNAME     = {Config().DB_USERNAME} 
DB_PASSWORD     = {Config().DB_PASSWORD} 
DISCORD_TOKEN   = {Config().DISCORD_TOKEN} 
COMMAND_PREFIX  = {Config().COMMAND_PREFIX} 
       """)
