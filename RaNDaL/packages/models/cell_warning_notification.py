import os
import time

import requests
import discord
from discord import Webhook, RequestsWebhookAdapter, File

from RaNDaL.packages.helpers.CWN_connection_config import config


class CellWarningNotification:
    def __init__(self):
        self.last_message_time = time.perf_counter()
        wb = config()
        self.webhook = Webhook.partial(wb['id'], wb['token'], adapter=RequestsWebhookAdapter())

    def alert(self):
        if self.last_message_time + 60 < time.perf_counter():
            self.webhook.send("CELL WARNING!")
            self.last_message_time = time.perf_counter()
