# RežisöörBot

Source code for RežisöörBot from [TheFilmChannel](https://t.me/thefilmchannel) in Telegram. In the future it will call for an external API but for now the bot will do all the business logic by itself.

As of right now it only sends a message with a film to a chat, but there are big plans in the future for mah boi the RežisöörBot.

## Requirements

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [tmdbv3api](https://github.com/AnthonyBloomer/tmdbv3api)
- Write permissions on the directory where the app is located (for the SQLite Database)

## Install Instructions

1. Copy env.base.py to env.py and fill the environment variables with your data.
2. Install the requirements mentioned above.

---

Run main.py. It will create a database on the first run, so make sure you have _write_ permissions.