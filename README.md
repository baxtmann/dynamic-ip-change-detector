# dynamic-ip-change-detector

A Fork of: [Ethical Punk's Dynamic IP Change Detector](https://github.com/ethicalpunk/dynamic-ip-change-detector)

A script that detects if your public IP was changed, and if so sends it to a discord webhook.

### Changes I've made:

- Dockerized The Script
  
- Added support to script for reading from system ENV Variables

- Added Cloudflare DDNS support
  

### Docker Image

You can pull the docker image from [this](https://hub.docker.com/r/baxtmann/ip-change-detector) dockerhub repository

For the script to work, you need to add an ENV varibale for the Discord webhook URL:

```sh
DISCORD_WEBHOOK = 'https://discord.com/WEBHOOKURLHERE'
```

### Cloudflare DDNS Implementation

This container now supports automatically updating DNS records in Cloudflare. It looks for any records with the old IP address and changes them to the new IP address.

To enable this feature, set an environment variable callled "DDNS=YES" to enable Cloudflare DDNS updates.

You'll also need to create an API key in Cloudflare, the minimum required permissions is RW access to zones you want to be auto updated.

Once you have your API key, set it via an environment variable called CLOUDFLARE_API_KEY

The script will also then send a webhook message notifying you that the domains have been updated.

If you have more than 20 domains in Cloudflare, you'll need to increase the amount of domains the script pulls, but updating the LIMIT environment variable.

To see a list of all supported ENV Vars, you can refer to config.env.example

### Redis Implementation
To help with bugs related to loss of internet connection, I've added Redis support so that the old IP can persist even if the script crashes, stops etc. All you need to do is install the base redis server, and store the IP as an env var called 'REDIS_HOST' and the script will take it from there. (note that it uses db 0 by default. ) I just use the default redis docker iamge which can be found here: https://hub.docker.com/_/redis