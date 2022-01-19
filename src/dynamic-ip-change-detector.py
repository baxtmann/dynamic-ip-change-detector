import urllib.request
import time
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

discord_webhook = "" # This variable is where you define your discord channel webhook

def webhook(content, url):
    webhook = DiscordWebhook(url=url)

    embed = DiscordEmbed(title='New IP detected', description='{}'.format(content), color='0xff0000')
    webhook.add_embed(embed)
    response = webhook.execute()

currentip = []

while True:
    endpoint = 'https://wtfismyip.com/text' # Do not change this variable unless you know what you're doing
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
