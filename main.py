from Data import Data
from Config import Config
from discord.ext import commands
from Model.Context import Context
from dateutil.parser import parse
from Helper import Helper
from datetime import datetime

bot = commands.Bot(command_prefix='!ass ')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# @bot.event
# async def on_message(message: discord.Message):
#     print('Message from {0.author}: {0.content}'.format(message))


@bot.command('add')
async def add(context: Context, subjectName: str = "", due_date: str = "", eventName: str = ""):
    """Add Due date          !ass add subject_name due_date event_name(opt)"""
    try:
        if not subjectName or not due_date:
            return await context.send(Helper.talkLikeABot(
                "🤢🤢 Hey you did not pass enough argument!\n"
                "!ass add subject_name due_date event_name (optional)"
            ))
        due = parse(due_date)
        if datetime.strptime(str(due).split(' ')[0], "%Y-%m-%d").date() < datetime.now().date():
            return await context.send(Helper.talkLikeABot(
                "Hmm... i dont quite get what is the date ... \n"
                "Either you enter wrong date format [Use this (2021-03-29)] \n"
                "Or you enter a date that is already pass "
            ))

        Data().add(context, subjectName, due_date, eventName)
        event = "[" + eventName + "]" if eventName != "" else ""
        await context.send(Helper.talkLikeABot(f"Due date for Subject:{subjectName}{event} on {due} has been added"))
    except Exception as e:
        await context.send(e)
        print(e)


@bot.command('all')
async def showAll(context: Context):
    """Find All Due date     !ass show all """
    try:
        dueDates = Data().getAll(context)
        if len(dueDates) == 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date setup yet"))

        await context.send(Helper.talkDueDateAsBot(dueDates))
    except Exception as e:
        await context.send(e)
        print(e)


@bot.command('find')
async def find(context: Context, subjectName: str):
    """Find Due date         !ass find subject_name """
    try:
        dueDates = Data().findBySubjectName(context, subjectName)
        if len(dueDates) == 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date name as : {subjectName}"))

        await context.send(Helper.talkDueDateAsBot(dueDates))

    except Exception as e:
        await context.send(e)


@bot.command('id')
async def find(context: Context, id: str):
    """Find Due date         !ass find subject_name """
    try:
        dueDates = Data().findById(context, id)
        if len(dueDates) == 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date name as : {id}"))

        await context.send(Helper.talkDueDateAsBot(dueDates))

    except Exception as e:
        await context.send(e)


@bot.command('change')
async def hole(context: Context, subjectID: str, subjectName: str = "", dueDate: str = "", eventName: str = ""):
    """Change Due Date Info  !ass change id subject_name due_date event_name"""
    try:
        dueDates = Data().findById(context, subjectID)
        if len(dueDates) == 0:
            return await context.send(Helper.talkLikeABot(f"There is no due date with id : {subjectID}"))
        Data().change(subjectID, subjectName, dueDate, eventName)

        await context.send(Helper.talkDueDateAsBot(f"Beep Bop ! Subject with id : '{subjectID}' has been deleted "))

    except Exception as e:
        await context.send(e)


@bot.command('hole')
async def hole(context: Context, subjectID: str):
    """Delete Due Date       !ass hole subject_id """
    try:
        Data().markAsDelete(context, subjectID)
        await context.send(Helper.talkDueDateAsBot(f"Beep Bop ! Subject with id : '{subjectID}' has been deleted "))
    except Exception as e:
        await context.send(e)


if __name__ == "__main__":
    bot.run(Config().DISCORD_TOKEN)
