import os
import requests
import json
from dotenv import load_dotenv
import CloudFlare
from discord_webhook import DiscordWebhook, DiscordEmbed
from urllib.request import Request, urlopen
# Standalone version of CF DDNS without the webhook functionality. 

load_dotenv(dotenv_path='config.env')

endpoint = "https://api.cloudflare.com/client/v4/"
CLOUDFLARE_API_KEY = os.environ['CLOUDFLARE_API_KEY']

#Don'y run without adding these values! These are automatically populated if using the dynamic-ip-change-detector.py script.
oldIP = ""
newIP = ""

cf = CloudFlare.CloudFlare()
zones = cf.zones.get()
for zone in zones:
    zone_id = zone['id']
    zone_name = zone['name']
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
        for dns_records in dns_records:
            if dns_records['type'] == "A":
                if dns_records['content'] == oldIP:
                    print(
                        dns_records['name'] + " " + dns_records['type'] + " " + dns_records['content'])
                    data_record = {
                        'name': dns_records['name'],
                        'type': dns_records['type'],
                        'content': newIP,
                        'proxied': dns_records['proxied']
                    }
                    try: 
                        cf.zones.dns_records.put(
                            zone_id, dns_records['id'], data=data_record)
                    except CloudFlare.exceptions.CloudFlareAPIError as e:
                                #send failure message
                                print (e,e)

    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records.get %d %s - api call failed' % (e, e))
