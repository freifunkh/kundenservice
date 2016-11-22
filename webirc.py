#!/usr/bin/python3
import sopel.module
import sopel.formatting

message = """Hey {0}!
Wir heißen Sie herzlich Wilkommen in unserem IRC-Chat.
Wir würden uns freuen, wenn Sie sich einen Spitznamen geben würden.
Beim Start des WebIRC werden sie aufgefordert einen Namen zu wählen. Das können sie beim nächsten Mal machen.
Vorerst reicht es, wenn Sie unten in die Chatzeile "/n IhrSpitzname" eingeben.
Noch ein paar Tipps, falls du zum ersten Mal in einem IRC-Chat unterwegs bist:
1. Bring ein bisschen Zeit mit, wenn du eine Frage stellst. Nicht jeder wird deine Frage sofort lesen.
2. Stell deine Frage direkt, ohne um Erlaubnis zu fragen, ob du eine Frage stellen darst.
Und nun viel Spaß beim freufunken! ;)
"""

@sopel.module.event('JOIN')
@sopel.module.rule('.*')
def write_to_webirc(bot, trigger):
    nick = trigger.nick

    if not nick.startswith('WebIRC'):
        return

    for line in message.split('\n'):
        bot.say(line.format(nick) + '\n', nick)
