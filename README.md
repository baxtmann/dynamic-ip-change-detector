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