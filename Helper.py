from Model.DueDate import DueDate


class Helper:
    @staticmethod
    def talkDueDateAsBot(dueDates: [DueDate]) -> str:
        temp = '```'
        for d in dueDates:
            event = "[" + d.title + "]" if d.title != "" else ""
            temp += f"[{d.id}] [{d.module_name}{event}] is Due on {d.due_date.split(' ')[0]} \t\t created by :" \
                    f"{d.created_by} \n"
        temp += '```'
        return temp

    @staticmethod
    def talkLikeABot(word: str) -> str:
        return f"```{word}```"
