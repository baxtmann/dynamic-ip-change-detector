import time
import json
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from urllib.request import Request, urlopen
import CloudFlare
from dotenv import load_dotenv
import redis
import sys
import ipaddress
load_dotenv(dotenv_path='config.env')
discord_webhook = os.environ['DISCORD_WEBHOOK']

# discord_webhook = "" You can use this if you don't want to use Docker ENV

endpoint = "https://api.cloudflare.com/client/v4/"
CLOUDFLARE_API_KEY = os.environ['CLOUDFLARE_API_KEY']
limit = os.environ['LIMIT']
REDIS_HOST = os.environ['REDIS_HOST']


def webhook(content, url):
    webhook = DiscordWebhook(url=url)

    embed = DiscordEmbed(title='New IP detected',
                         description='{}'.format(content), color='0xff0000')
    webhook.add_embed(embed)
    response = webhook.execute()


def webhook_DDNS(content, url):
    webhook = DiscordWebhook(url=url)

    embed = DiscordEmbed(title='CloudFlare DDNS Updated',
                         description='{}'.format(content), color='0xff0000')
    webhook.add_embed(embed)
    response = webhook.execute()


def webhook_ERROR(content, url):
    webhook = DiscordWebhook(url=url)

    embed = DiscordEmbed(title='Error Encountered',
                         description='{}'.format(content), color='0xff0000')
    webhook.add_embed(embed)
    response = webhook.execute()


currentip = []

while True:
    # Do not change this variable unless you know what you're doing
    endpoint = 'https://ip.edge9.workers.dev/'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    request = Request(endpoint, headers=hdr)
    data = urlopen(request).read()
    ip = data.decode().strip()
    count = 0
    print(ip)
    # init redis connection
    r = redis.Redis(host=REDIS_HOST, port=6379,
                    charset="UTF-8", decode_responses=True, db=0)
    redisIPOld = r.get('ip')
    print("RedisIPOld: " + str(redisIPOld))

    if ip == redisIPOld:
        if ip in currentip:
            pass
    else:
        # this prevents the script from wiping dns records when it runs for the first time (ensures old ip is not empty, if it is the script will try and change all ips)
        if count == 0:
            oldIP = ip
            count = count + 1
        newIP = ip
        currentip = []
        currentip.append(ip)
        webhook(f"**New IP**: `{ip}`", discord_webhook)
        if (os.environ['DDNS'] == 'yes'):
            print("Starting CF DDNS Update")
            cf = CloudFlare.CloudFlare()
            zones = cf.zones.get(params={'per_page': limit})
            for zone in zones:
                zone_id = zone['id']
                zone_name = zone['name']
                try:
                    dns_records = cf.zones.dns_records.get(
                        zone_id, params={'per_page': limit})
                    for dns_records in dns_records:
                        if dns_records['type'] == "A":
                            if dns_records['content'] == redisIPOld:
                                print(
                                    "OLD: " + dns_records['name'] + " " + dns_records['type'] + " " + dns_records['content'])
                                data_record = {
                                    'name': dns_records['name'],
                                    'type': dns_records['type'],
                                    'content': newIP,
                                    'proxied': dns_records['proxied']
                                }
                                try:
                                    cf.zones.dns_records.put(
                                        zone_id, dns_records['id'], data=data_record)
                                    webhook_DDNS(
                                        f"**Updated**: `{dns_records['name']}`", discord_webhook)
                                    print(
                                        "NEW: " + dns_records['name'] + " " + dns_records['type'] + " " + data_record['content'])
                                except CloudFlare.exceptions.CloudFlareAPIError as e:
                                    # send failure message to discord
                                    webhook_ERROR(f"`{e, e}`", discord_webhook)

                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    exit('/zones/dns_records.get %d %s - api call failed' % (e, e))
            # getting IPRedis ready for redis. We will first check to make sure it's a valid IP address
            try:
                ipaddress.ip_address(ip)
                print("Valid IP Address")
                IPRedis = ip
            except ValueError:
                print("Invalid IP Address, we will not save this to redis. Instead we will save 1.1.1.1")
                #we do this so that next time the script runs, it'll be forced to update the IP address. If it is still invalid when it tries again, CF will reject it if it's not a valid IP. 
                IPRedis = "1.1.1.1"
            # here we save the current IP to redis, for the next check.
            r.set('ip', IPRedis)
            print("IP Saved to Redis!")
    # Waits for 60 seconds until it checks if the IP was changed again. Respect rate limiting and keep this number as high as possible.
    time.sleep(60)
