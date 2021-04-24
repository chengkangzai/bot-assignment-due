from Data import Data
from Config import Config
from discord.ext import commands
from Model.Context import Context
from dateutil.parser import parse
from Helper import Helper
from datetime import datetime

bot = commands.Bot(command_prefix=Config().COMMAND_PREFIX + " ")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Bot started and listening to command prefix : ' + Config().COMMAND_PREFIX)
    print('------')


# @bot.event
# async def on_message(message: discord.Message):
#     print('Message from {0.author}: {0.content}'.format(message))


@bot.command('add')
async def add(context: Context, subjectName: str = "", due_date: str = "", eventName: str = ""):
    """Add Due date          !ass add subject_name due_date event_name(opt)"""
    if not subjectName or not due_date:
        return notEnoughArgs(context)

    try:
        due = datetime.strptime(str(parse(due_date)).split(' ')[0], "%Y-%m-%d")
        if due.date() < datetime.now().date():
            return await context.send(Helper.talkLikeABot(
                "Hmm... i dont quite get what is the date ... \n"
                "Either you enter wrong date format [Use '2021-03-29' 29-03-2021] \n"
                "Or you enter a date that is already pass "
            ))

        Data().add(context, subjectName, due_date, eventName)

        event = "[" + eventName + "]" if eventName != "" else ""
        return await context.send(Helper.talkLikeABot(f"Due date for Subject:{subjectName}{event} on "
                                                      f"{str(due).split(' ')[0]} has been added"))
    except Exception as e:
        return await context.send(e)


@bot.command('all')
async def showAll(context: Context):
    """Find All Due date     !ass show all """
    try:
        dueDates = Data().getAll(context)
        if len(dueDates) == 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date setup yet"))

        return await context.send(Helper.talkDueDateAsBot(dueDates))
    except Exception as e:
        return await context.send(e)


@bot.command('find')
async def find(context: Context, subjectName: str):
    """Find Due date         !ass find subject_name """
    if not subjectName:
        return notEnoughArgs(context)

    try:
        dueDates = Data().findBySubjectName(context, subjectName)
        if len(dueDates) == 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date name as : {subjectName}"))

        return await context.send(Helper.talkDueDateAsBot(dueDates))

    except Exception as e:
        return await context.send(e)


@bot.command('id')
async def findID(context: Context, dueDateID: str):
    """Find Due date         !ass find subject_name """
    if not dueDateID:
        return notEnoughArgs(context)

    try:
        dueDates = Data().findById(context, dueDateID)
        if len(dueDates) == 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date id as : {dueDateID}"))

        return await context.send(Helper.talkDueDateAsBot(dueDates))

    except Exception as e:
        return await context.send(e)


@bot.command('change')
async def change(context: Context, subjectID: str, subjectName: str = "", dueDate: str = "", eventName: str = ""):
    """Change Due Date Info  !ass change id subject_name due_date event_name"""
    if not subjectID:
        return notEnoughArgs(context)

    try:
        dueDates = Data().findById(context, subjectID)
        if len(dueDates) == 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date with id : {subjectID}"))

        check = dueDates[0]
        if check.module_name == subjectName and check.due_date == parse(dueDate).date() and check.title == eventName:
            return await context.send(Helper.talkLikeABot("Are you try to change it to same content !? NO"))

        db = Data().change(context, subjectID, subjectName, dueDate, eventName)

        if db.cursor.rowcount <= 0:
            return await context.send("Problem Occur")

        return await context.send(Helper.talkLikeABot(f"Beep Bop ! Due Date with id : '{subjectID}' has been change "))

    except Exception as e:
        return await context.send(e)


@bot.command('hole')
async def hole(context: Context, subjectID):
    """Delete Due Date       !ass hole subject_id """
    if not subjectID:
        return notEnoughArgs(context)

    try:
        if len(Data().findById(context, subjectID)) <= 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date with id : {subjectID}"))

        Data().markAsDelete(context, subjectID)
        return await context.send(Helper.talkLikeABot(f"Beep Bop ! Due Date with id : '{subjectID}' has been deleted "))
    except Exception as e:
        return await context.send(e)


@bot.command('about')
async def about(context: Context):
    """Show Info of this bot :3 """
    version = '1.0.1'
    await context.send(f"""
    Assignment Due Date Bot v{version}
Hi there ! This project is created by chengkangzai (https://github.com/chengkangzai)
Any bug report can create a issue at here https://tinyurl.com/assbotIssues
    """)


async def notEnoughArgs(context: Context):
    return await context.send(Helper.talkLikeABot(
        "🤢🤢 Hey you did not pass enough argument!\n"
        "!ass add subject_name due_date event_name (optional)"
    ))


if __name__ == "__main__":
    bot.run(Config().DISCORD_TOKEN)
