from Model.Context import Context
from Config import Config
import mysql.connector


class AngryData:
    def __init__(self):
        self.con = mysql.connector.connect(
            host=Config().DB_HOST,
            user=Config().DB_USERNAME,
            password=Config().DB_PASSWORD,
            database=Config().DB_DATABASE
        )
        self.cursor = self.con.cursor(buffered=True)
        print("Opened database successfully")

    def setUpTable(self):
        print("Creating Table")
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS guild_angry(
            id                  INT                     PRIMARY KEY AUTO_INCREMENT ,
            guild_id            VARCHAR(255)                    NULL
            );
        ''')
        self.con.commit()
        print("Table created successfully")
        return self

    def setAngry(self, context: Context):
        sql = f"""INSERT INTO guild_angry(guild_id) VALUES  ({context.guild.id})"""
        self.cursor.execute(sql)
        self.con.commit()

        if self.cursor.rowcount <= 0:
            raise Exception("Opps! There is some problem adding your record. Contact Bot maintainer to get helps")
        return self

    def setNotAngry(self, context: Context):
        sql = f"""DELETE FROM guild_angry WHERE guild_id={context.guild.id}"""
        self.cursor.execute(sql)
        self.con.commit()

        if self.cursor.rowcount <= 0:
            raise Exception("Opps! There is some problem adding your record. Contact Bot maintainer to get helps")
        return self

    def isGuildAngry(self, context: Context):
        sql = f"""SELECT * FROM guild_angry WHERE guild_id={context.guild.id}; """
        self.cursor.execute(sql)
        print(context.guild.id)
        record = self.cursor.rowcount
        return record == 1


if __name__ == "__main__":
    print("1. Initial Setup")
    print("2. Get DB Detail")
    operation = input("What do you want !?")
    if operation == "1":
        AngryData().setUpTable()
    elif operation == "2":
        print(f"""Operating under 
DB_HOST     = {Config().DB_HOST}
DB_USERNAME = {Config().DB_USERNAME}
DB_PASSWORD = {Config().DB_PASSWORD}
DB_DATABASE = {Config().DB_DATABASE}
       """)
    else:
        exit(print("Invalid Input"))
