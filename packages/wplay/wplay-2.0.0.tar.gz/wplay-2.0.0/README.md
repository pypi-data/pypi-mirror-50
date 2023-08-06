# whatsapp-play

[![Downloads](https://pepy.tech/badge/wplay)](https://pepy.tech/project/wplay)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/749acf4cad424fbeb96a412963aa83ea)](https://app.codacy.com/app/rpotter12/whatsapp-play?utm_source=github.com&utm_medium=referral&utm_content=rpotter12/whatsapp-play&utm_campaign=Badge_Grade_Settings)
[![PyPi](https://img.shields.io/badge/pypi-v1.0.6-blue.svg)](https://pypi.org/project/wplay/)
[![codecov](https://codecov.io/gh/rpotter12/whatsapp-play/branch/master/graph/badge.svg)](https://codecov.io/gh/rpotter12/whatsapp-play)
[![twitter](https://img.shields.io/twitter/url/https/github.com/rpotter12/whatsapp-play.svg?style=social)](https://twitter.com/rpotter121998)
[![HitCount](http://hits.dwyl.io/rpotter12/whatsapp-play.svg)](http://hits.dwyl.io/rpotter12/whatsapp-play)

It is command line software through which you can play with your WhatsApp. It is having different options to play with your WhatsApp like message blast, online tracking, whatsapp chat.. This software aims to provide all facilities which we can do with WhatsApp. This CLI software does not require any API key for the execution.

***wchat*** stands for WhatsApp chat. Through this you can chat with your WhatsApp contact directly from the command line.

***onlinetracker*** tracks the online and offline timings of your WhatsApp contact. It will check the online status and will immediately stores that data into a .txt file. Blog link: [https://github.com/rpotter12/rpotter12.github.io/blob/master/blogs/blog3-tracking-26-07-2019.md](https://github.com/rpotter12/rpotter12.github.io/blob/master/blogs/blog3-tracking-26-07-2019.md)

***messageblast*** is a message bomb script. It sends messages to your WhatsApp contact continously. The number of messages is decided by you. You can blast infinite number of messages to your WhatsApp contact.

***savechat*** is a script to save the chat of the person. It saves all the messages with that person in message.txt file.

---

## Installation
- `pip3 install wplay`

## Usage
```
usage: wplay [-h] (-wc | -wb | -wt| -ws) NAME

WhatApp-play

positional arguments:
  NAME           contact name of the target

optional arguments:
  -h, --help     show this help message and exit
  -wc, --wchat   chatting from command line
  -wb, --wblast  message blast to a person
  -wt, --wtrack  track online status of person
  -ws, --wsave   save the whole chat of a person
```
Example - `wplay -wt "target_name_of_your_whatsapp_contact"`

## Things to do
- [x] onlinetracker script - to track the online/offline status.([issue #3](https://github.com/rpotter12/whatsapp-play/issues/3))
- [x] wchat script - to chat with contact from command line.
- [x] messageblast script - to send message repeatedly to a person.
- [x] argument parser to connect all scripts to one script.([pull #9](https://github.com/rpotter12/whatsapp-play/pull/9))
- [ ] telegram bot script for onlinetracker to send the status online/offline status to telegram bot.([issue #4](https://github.com/rpotter12/whatsapp-play/issues/4))
- [x] improve onlinetracker script.([pull #9](https://github.com/rpotter12/whatsapp-play/pull/9))
- [x] improve messageblast script.
- [x] improve wchat script for chatting.([pull #10](https://github.com/rpotter12/whatsapp-play/pull/10))
- [x] a sound notification in pc system when the person gets online.([issue #22](https://github.com/rpotter12/whatsapp-play/issues/22))
- [ ] script to save the whole chat of a person.([issue #12](https://github.com/rpotter12/whatsapp-play/issues/12))
- [ ] docker image for whatsapp-play.([issue #21](https://github.com/rpotter12/whatsapp-play/issues/21))
- [ ] keep a record of states of multiple users in csv, for further analysis([issue #15](https://github.com/rpotter12/whatsapp-play/issues/15))
- [ ] proper option to exit the running program([issue #19](https://github.com/rpotter12/whatsapp-play/issues/19))
- [x] save the status.txt file of onlinetracking in separate wplay folder([issue #24](https://github.com/rpotter12/whatsapp-play/issues/24))
- [ ] script to find the location of the person([issue #31](https://github.com/rpotter12/whatsapp-play/issues/31))
- [ ] .travis.yml script for travis check([issue #20](https://github.com/rpotter12/whatsapp-play/issues/20))<br>
(If you have any new idea for this software, please open issue for that :) )

## Disclaimer
This software is for educational purpose only. Keeping eye on a innocent person can make person's life stressful.

## License
[![License](https://img.shields.io/github/license/rpotter12/whatsapp-play.svg)](https://github.com/rpotter12/whatsapp-play/blob/master/README.md)

***If you like the project, support us by star***
