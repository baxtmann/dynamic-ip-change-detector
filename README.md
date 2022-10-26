# dynamic-ip-change-detector

A Fork of: [Ethical Punk's Dynamic IP Change Detector](https://github.com/ethicalpunk/dynamic-ip-change-detector)

A script that detects if your public IP was changed, and if so sends it to a discord webhook.

### Changes I've made: 

- Dockerized The Script
- Added support to script for reading from system ENV Variables

### Docker Image

You can pull the docker image from [this](https://hub.docker.com/r/baxtmann/ip-change-detector) dockerhub repository

For the script to work, you need to add a ENV varibale for the Discord webhook URL: 

``` sh
DISCORD_WEBHOOK = 'https://discord.com/WEBHOOKURLHERE'
```

### Cloudflare DDNS Implementation
This container now supports automatically updating DNS records in Cloudflare. It looks for any records with the old IP address and changes them to the new IP address. 

To enable this feature, set an environment variable callled "DDNS=YES" to enable Cloudflare DDNS updates. 
You'll also need to create an API key in Cloudflare, the minimum required permissions is RW access to zones you want to be auto updated. 

Once you have your API key, set it via an environment variable called CLOUDFLARE_API_KEY
The script will also then send a webhook message notifying you that the domains have been updated. 