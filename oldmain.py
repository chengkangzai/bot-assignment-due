# import discord
# from discord.ext import commands
#
# from Config import Config
#
#
# class MyClient(discord.Client):
#
#     async def on_ready(self):
#         print('Logged on as {0}!'.format(self.user))
#
#     async def on_message(self, message: discord.Message):
#         print('Message from {0.author}: {0.content}'.format(message))
#         messageContent = str(message.content)
#         if messageContent.startswith("!ass"):
#
#             await message.channel.send("Hello")
#         return
#
#
# if __name__ == "__main__":
#     MyClient().run(Config().DISCORD_TOKEN)
