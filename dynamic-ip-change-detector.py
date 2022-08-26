import urllib.request
import time
import json
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

discord_webhook = os.environ['DISCORD_WEBHOOK']

#discord_webhook = "" You can use this if you don't want to use Docker ENV

def webhook(content, url):
    webhook = DiscordWebhook(url=url)

    embed = DiscordEmbed(title='New IP detected', description='{}'.format(content), color='0xff0000')
    webhook.add_embed(embed)
    response = webhook.execute()

currentip = []

while True:
    endpoint = 'https://ip.edge9.workers.dev/' # Do not change this variable unless you know what you're doing
    data = urllib.request.urlopen(endpoint).read()
    ip = data.decode().strip()

    print(ip)

    if ip in currentip:
        pass
    else:
        currentip = []
        currentip.append(ip)
        webhook(f"**New IP**: `{ip}`" , discord_webhook)

    time.sleep(60) # Waits for 60 seconds till it checks if the IP was changed again. Respect rate limiting and keep this number as high as possible.