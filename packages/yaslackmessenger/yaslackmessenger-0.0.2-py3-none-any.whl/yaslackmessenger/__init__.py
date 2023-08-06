import requests
COLORS = {"red": "#FF1111",
          "green": "#11FF11",
          "blue": "#281CB2",
          "yellow": "#D9E50E"}


class Slacker:
    def __init__(self, name, channel):
        self.channel = channel
        self.name = name

    @staticmethod
    def getcolor(color):
        if color in COLORS.keys():
            return COLORS[color]
        return color
 
    def slackerror(self, error, color="red"):
        color = self.getcolor(color)
        return {
             "fallback": "{0} Error".format(self.name),
             "color": color,
             "pretext": " {0} Error:".format(self.name),
             "author_name": "",
             "text": error or "",
         }
 
    def slackinfo(self, info, color="green"):
        color = self.getcolor(color)
        return {
            "fallback": "{0} Info".format(self.name),
            "color": color,
            "pretext": "{0} Info:".format(self.name),
            "author_name": "",
            "text": info or "",
        }

    def slackit(self, text, attachments=None):
        attachments = attachments or []
        j = dict(text=text, attachments=attachments)
        return requests.post(self.channel, json=j)




