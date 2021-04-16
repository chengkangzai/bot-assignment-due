from dateutil.parser import parse

from Model.DueDate import DueDate
from Model.Context import Context
from Config import Config
import mysql.connector


class Data:

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
        CREATE TABLE IF NOT EXISTS assignment_due(
            id                  INT                     PRIMARY KEY AUTO_INCREMENT ,
            subject_name        VARCHAR(255)            NOT NULL,
            title               VARCHAR(255)            NULL,
            due_date            DATE                    NOT NULL,
            guild_id            VARCHAR(255)                    NULL ,
            channel_id          VARCHAR(255)                    NULL,
            created_by          VARCHAR(255)            DEFAULT NULL ,
            created_at          TIMESTAMP               DEFAULT CURRENT_TIMESTAMP,
            deleted_by          VARCHAR(255)            DEFAULT NULL ,
            deleted_at          TIMESTAMP               DEFAULT NULL
            );
        ''')
        self.con.commit()
        print("Table created successfully")
        return self

    def __seedTestData(self):
        subjectName = "MAR"
        eventName = "TEST TEST"
        due = parse("2021-01-01")

        print(f"""Seeding Data due date of 
subjectName ={subjectName}
eventName   ={eventName}
due         ={due}   
        """)

        self.cursor.execute(f"""
                    INSERT INTO assignment_due(subject_name,title,due_date,guild_id,channel_id,created_by) VALUES 
                                ("{subjectName}","{eventName}", "{due}","123","123","ppl")
                    """)
        self.con.commit()
        if self.cursor.rowcount <= 0:
            raise Exception("There is no row effected")

        print("TEST 1 Seed Data to table :: PASSED")
        return self

    def __readTestData(self):
        self.cursor.execute(f"""
                   SELECT id, subject_name, title, due_date, guild_id, channel_id, created_by 
                       FROM assignment_due 
                   """)
        if self.cursor.rowcount <= 0:
            raise Exception("No Record")

        dueDates = self.cursor.fetchall()
        for dueDate in dueDates:
            print(dueDate)
        print("TEST 2 Seed Data to table :: PASSED")
        return self

    def __readSingle(self):
        self.cursor.execute(f"""
                SELECT id, subject_name, title, due_date, guild_id, channel_id ,created_by
                    FROM assignment_due 
                        WHERE id=11
                        ORDER BY due_date
                        LIMIT 1
                """)

        if self.cursor.rowcount <= 0:
            raise Exception("No Record")

        dueDates = self.cursor.fetchone()
        for dueDate in dueDates:
            print(dueDate)

        return self

    def __updateSeedData(self):
        subjectName = "MAR"
        eventName = "AFTER UPDATE TEST TEST"
        due = parse("2021-01-01")
        print(f"""Seeding Data due date of 
subjectName ={subjectName}
eventName   ={eventName}
due         ={due}   
                """)
        self.cursor.execute(f"""
            UPDATE assignment_due
                SET subject_name="{subjectName}",title ="{eventName}",due_date ="{due}"
                WHERE id = "1"
               """)
        self.con.commit()
        print("TEST 3 Update Seed Data to table :: PASSED")
        return self

    def __del__(self):
        self.cursor.close()
        self.con.close()

    def test(self):
        self.__seedTestData() \
            .__readTestData() \
            .__updateSeedData() \
            .__readTestData()

    def add(self, context: Context, subjectName: str, due_date: str, eventName: str = "", ):
        due = parse(due_date)
        sql = "INSERT INTO assignment_due(subject_name,title,due_date,guild_id,channel_id,created_by) " \
              "VALUES  (%s,%s,%s,%s,%s,%s)"
        val = (subjectName, eventName, due, context.guild.id, context.channel.id, context.author.name)
        self.cursor.execute(sql, val)
        self.con.commit()

        if self.cursor.rowcount <= 0:
            raise Exception("Opps! There is some problem adding your record. Contact Bot maintainer to get helps")
        return self

    def change(self, context: Context, dueDateId: str, subjectName: str, due_date: str, eventName: str = "", ):
        due = parse(due_date)
        sql = "UPDATE assignment_due SET subject_name=%s,title =%s,due_date =%s WHERE guild_id=%s AND id = %s"
        val = (subjectName, eventName, str(due), context.guild.id, dueDateId)
        self.cursor.execute(sql, val)
        self.con.commit()
        return self

    def findBySubjectName(self, context: Context, subjectName: str) -> [DueDate]:
        temp = []
        sql = "SELECT id, subject_name, title,due_date, guild_id, channel_id, created_by, deleted_at " \
              "FROM assignment_due WHERE guild_id=%s AND subject_name=%s AND deleted_at IS NULL ORDER BY due_date"
        val = (context.guild.id, subjectName)
        self.cursor.execute(sql, val)

        if self.cursor.rowcount <= 0:
            return temp

        dueDates = self.cursor.fetchall()
        for dueDate in dueDates:
            temp.append(DueDate(dueDate[0], dueDate[1], dueDate[2], dueDate[3], dueDate[4], dueDate[5], dueDate[6]))
        return temp

    def findById(self, context: Context, id: str) -> [DueDate]:
        temp = []
        sql = "SELECT id, subject_name, title,due_date, guild_id, channel_id, created_by, deleted_at " \
              "FROM assignment_due WHERE guild_id=%s AND id=%s AND deleted_at IS NULL ORDER BY due_date"
        val = (context.guild.id, id)
        self.cursor.execute(sql, val)

        if self.cursor.rowcount <= 0:
            return temp

        dueDates = self.cursor.fetchall()
        for dueDate in dueDates:
            temp.append(DueDate(dueDate[0], dueDate[1], dueDate[2], dueDate[3], dueDate[4], dueDate[5], dueDate[6]))
        return temp

    def getAll(self, context: Context) -> [DueDate]:
        temp = []
        sql = "SELECT id, subject_name, title, due_date, guild_id, channel_id, created_by, deleted_at " \
              f"""FROM assignment_due WHERE guild_id={context.guild.id}  AND deleted_at IS NULL"""
        self.cursor.execute(sql)

        if self.cursor.rowcount <= 0:
            return temp

        dueDates = self.cursor.fetchall()
        for dueDate in dueDates:
            temp.append(DueDate(dueDate[0], dueDate[1], dueDate[2], dueDate[3], dueDate[4], dueDate[5], dueDate[6]))
        return temp

    def markAsDelete(self, context: Context, dueDateId: str):
        sql = "UPDATE assignment_due  SET deleted_at = CURRENT_TIMESTAMP, deleted_by=%s " \
              "WHERE guild_id=%s AND id=%s AND deleted_at IS NULL "
        val = (context.author.name, context.guild.id, dueDateId)
        self.cursor.execute(sql, val)
        self.con.commit()
        if self.cursor.rowcount <= 0:
            raise Exception("Opps your due date isnt going anywhere because technical problem faced."
                            " Contact bot maintainer.")
        return self


if __name__ == "__main__":
    print("1. Initial Setup")
    print("2. Do test on DB")
    print("3. Get DB Detail")
    operation = input("What do you want !?")
    if operation == "1":
        Data().setUpTable()
    elif operation == "2":
        Data().test()
    elif operation == "3":
        print(f"""Operating under 
DB_HOST     = {Config().DB_HOST}
DB_USERNAME = {Config().DB_USERNAME}
DB_PASSWORD = {Config().DB_PASSWORD}
DB_DATABASE = {Config().DB_DATABASE}
       """)
    else:
        exit(print("Invalid Input"))
