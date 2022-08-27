import time
import json
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from urllib.request import Request, urlopen

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
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    request = Request(endpoint, headers=hdr)
    data = urlopen(request).read()
    ip = data.decode().strip()

    print(ip)

    if ip in currentip:
        pass
    else:
        currentip = []
        currentip.append(ip)
        webhook(f"**New IP**: `{ip}`" , discord_webhook)

    time.sleep(60) # Waits for 60 seconds till it checks if the IP was changed again. Respect rate limiting and keep this number as high as possible.