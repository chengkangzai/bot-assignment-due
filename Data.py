import sqlite3
from dateutil.parser import parse
from Model.DueDate import DueDate
from Model.Context import Context


class Data:
    databaseName = 'database.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.databaseName)
        print("Opened database successfully")

    def __setUpTable(self):
        self.conn.execute('''
        CREATE TABLE assignment_due(
            id                  INTEGER         PRIMARY KEY AUTOINCREMENT ,
            subject_name        TEXT            NOT NULL,
            title               TEXT            NULL,
            due_date            DATE            NOT NULL,
            guild_id            INTEGER         NULL ,
            channel_id          INTEGER         NULL,
            created_by          TEST            DEFAULT "",
            created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
            deleted_by          TEXT            DEFAULT "",
            deleted_at          TIMESTAMP       DEFAULT ""
            );
        ''')
        self.conn.commit()
        return self

    def __seedTestData(self):
        self.conn.execute("""
        INSERT INTO assignment_due(subject_name,title,due_date,guild_id,channel_id) VALUES 
                                ("RMCT","Progression Check 1", "2/04/2021",1,1)
        """)
        self.conn.commit()
        return self

    def __readTestData(self):
        dueDates = self.conn.execute("SELECT id,intake,subject_name,title,due_date FROM assignment_due")
        for row in dueDates:
            print("ID" + str(row[0]))
            print("module_name" + row[2])
            print("title" + row[3])
            print("due_date" + row[4])
        return self

    def test(self):
        self.__setUpTable() \
            # .__seedTestData() \
        # .__readTestData()

    def add(self, context: Context, subjectName: str, due_date: str, eventName: str = "", ):
        due = parse(due_date)
        self.conn.execute(f"""
            INSERT INTO assignment_due(subject_name,title,due_date,guild_id,channel_id,created_by) VALUES 
                        ("{subjectName}","{eventName}", "{due}","{context.guild.id}","{context.channel.id}","{context.author.name}")
            """)
        self.conn.commit()
        return self.conn

    def change(self, dueDateId: str, subjectName: str, due_date: str, eventName: str = "", ):
        due = parse(due_date)
        self.conn.execute(f"""
        UPDATE assignment_due
            SET subject_name="{subjectName}",title ="{eventName}",due_date ="{due}"
            WHERE id = "{dueDateId}"
           """)
        self.conn.commit()
        return self

    def findBySubjectName(self, context: Context, subjectName: str) -> [DueDate]:
        temp = []
        dueDates = self.conn.execute(f"""
        SELECT id, subject_name, title,due_date, guild_id, channel_id, created_by
            FROM assignment_due 
                WHERE guild_id="{context.guild.id}" 
                AND subject_name="{subjectName}"  
                ORDER BY due_date
        """)
        for dueDate in dueDates:
            temp.append(DueDate(dueDate[0], dueDate[1], dueDate[2], dueDate[3], dueDate[4], dueDate[5], dueDate[6]))
        return temp

    def findById(self, context: Context, id: str) -> [DueDate]:
        temp = []
        dueDates = self.conn.execute(f"""
        SELECT id, subject_name, title, due_date, guild_id, channel_id ,created_by
            FROM assignment_due 
                WHERE guild_id="{context.guild.id}" 
                AND id="{id}"  
                ORDER BY due_date
        """)
        for dueDate in dueDates:
            temp.append(DueDate(dueDate[0], dueDate[1], dueDate[2], dueDate[3], dueDate[4], dueDate[5], dueDate[6]))
        return temp

    def getAll(self, context: Context) -> [DueDate]:
        temp = []
        dueDates = self.conn.execute(f"""
           SELECT id, subject_name, title, due_date, guild_id, channel_id, created_by 
               FROM assignment_due 
                   WHERE guild_id="{context.guild.id}" 
                   AND deleted_at=""
                   ORDER BY due_date
           """)
        for dueDate in dueDates:
            temp.append(DueDate(dueDate[0], dueDate[1], dueDate[2], dueDate[3], dueDate[4], dueDate[5], dueDate[6]))
        return temp

    def markAsDelete(self, context: Context, dueDateId: str):
        self.conn.execute(f"""
        UPDATE assignment_due 
            SET deleted_at = CURRENT_TIMESTAMP, deleted_by = "{context.author}" 
            WHERE id="{dueDateId}"
        """)
        self.conn.commit()
        return self


if __name__ == "__main__":
    Data().test()
