#!/usr/bin/python3
import sopel.module
import sopel.formatting

message = """Hey {0}!
Wir heißen Sie herzlich Wilkommen in unserem IRC-Chat.
Wir würden uns freuen, wenn Sie sich einen Spitznamen geben würden.
Beim Start des WebIRC werden Sie aufgefordert einen Namen zu wählen. Das können Sie beim nächsten Mal machen.
Vorerst reicht es, wenn Sie unten in die Chatzeile "/n IhrSpitzname" eingeben.
Noch ein paar Tipps, falls Sie zum ersten Mal in einem IRC-Chat unterwegs sind:
1. Bringen Sie ein bisschen Zeit mit, wenn Sie eine Frage stellen. Nicht jeder wird Ihre Frage sofort lesen.
2. Stellen Sie Ihre Frage direkt, ohne um Erlaubnis zu bitten, ob Sie eine Frage stellen dürfen.
Und nun viel Spaß beim Freufunken! ;)
"""

@sopel.module.event('JOIN')
@sopel.module.rule('.*')
def write_to_webirc(bot, trigger):
    nick = trigger.nick

    if not nick.startswith('WebIRC'):
        return

    for line in message.split('\n'):
        bot.notice(line.format(nick) + '\n', nick)
