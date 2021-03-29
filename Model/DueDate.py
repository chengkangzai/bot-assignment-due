class DueDate:

    def __init__(self, idd: str, module_name: str, title: str, due_date: str, guild_id: str, channel_id: str,
                 created_by: str):
        self.id = idd
        self.module_name = module_name
        self.title = title
        self.due_date = due_date
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.created_by = created_by
