from dotenv import dotenv_values


class Config:
    def __init__(self):
        env = dotenv_values(".env")
        self.DEBUG = env.get("DEBUG")
        self.DISCORD_TOKEN = env.get("DISCORD_TOKEN")
