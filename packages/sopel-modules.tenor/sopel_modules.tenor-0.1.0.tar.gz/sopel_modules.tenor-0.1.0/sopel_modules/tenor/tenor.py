# coding=utf-8

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)


import random

from sopel import module
from sopel.config.types import StaticSection, ValidatedAttribute

import requests


class TenorSection(StaticSection):
    api_key = ValidatedAttribute('api_key', str)


def setup(bot):
    bot.config.define_section('tenor', TenorSection)


def configure(config):
    config.define_section('api_key', TenorSection)
    config.tenor.configure_setting('api_key', 'Tenor api key')


def template_endpoint(search_term, api_key):
    endpoint_template = 'https://api.tenor.com/v1/search?q={}&key={}&limit=10'
    endpoint = endpoint_template.format(search_term, api_key)

    return endpoint


def get_gifs_from_json(j):
    return [i['media'][0]['gif']['url'] for i in j['results']]


@module.commands('gif')
def gif(bot, trigger):
    search_term = trigger.group(2)

    if not search_term:
        bot.say('Usage: gif <search_term>')
        return

    api_key = bot.config.tenor.api_key
    endpoint = template_endpoint(search_term, api_key)

    r = requests.get(endpoint)
    gifs = get_gifs_from_json(r.json())

    bot.say(random.choice(gifs))
