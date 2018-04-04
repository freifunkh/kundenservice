#!/usr/bin/python

import sopel.module
import sopel.formatting
import requests
from collections import namedtuple

def configure(config):
    # TOOD
    pass

def setup(bot):
    global channel, influx
    channel = bot.config.freifunkh.channel
    if channel is None:
        print("warning: you need to specify freifunkh.channel in your config")

    influx = dict(
        url=bot.config.freifunkh.influx_url,
        passwd=bot.config.freifunkh.influx_pass,
        user=bot.config.freifunkh.influx_user
    )

def influx_q(query):
    r = requests.get(influx['url'],
                     params={'q': query },
                     auth=(influx['user'], influx['passwd']))
    return r.json()

def series_names():
    q = influx_q('SHOW SERIES')
    
    series = q['results'][0]['series'][0]['values']

    series =  [s[0].split(',')[0] for s in series]

    series = filter(lambda s: s.startswith('nodemonitoring_'), series)

    # return unique
    return list(set(series))

def get_series(name):
    q = influx_q('SELECT "Bool_value" FROM "{name}" WHERE time >= now() - 2m GROUP BY "supernode", "tester"'.format(name=name))

    return q

def test(name):
    series = get_series(name)['results'][0]['series']

    for s in series:
        bool_index = s['columns'].index('Bool_value')
        time_index = s['columns'].index('time')

        tags = s['tags']

        last_value = s['values'][-1]

        yield (tags, last_value[bool_index], last_value[time_index])


previous_status = {}
statkey = namedtuple('statkey', ['name', 'supernode', 'tester'])

@sopel.module.interval(60)
def test_all(bot):
    names = series_names()

    for name in names:
        for tags, ok, time in test(name):
            k = statkey(name=name, supernode=tags['supernode'], tester=tags['tester'])
            retries = 0

            if k in previous_status:
                # if the current and the last test result do not vary
                if previous_status[k]['ok'] == ok:
                    retries = previous_status[k]['retries'] + 1

                # if everything just went back to normal or if the test failed n times in a row
                if retries == 0 and ok or retries == 2 and not ok:
                    write_msg(bot, k, ok, time)
            
            if k not in previous_status:
                if ok == False:
                    # write_msg(bot, k, ok, time)
                    pass

            previous_status[k] = dict(ok=ok, last_time=time, retries=retries)

def write_msg(bot, k, ok, time):
    okstr = '[OK]' if ok else '[ALERT]'
    bot.msg(channel, "{} {k.name} sn: {k.supernode} tester: {k.tester}".format(okstr, k=k))
