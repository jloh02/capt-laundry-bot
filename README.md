# CAPT Laundry Bot

Laundry bot for the management of

## Setup

### Requirements

- Python 3.12
- Docker (Only for deployment)

### Telegram Bot Setup (Local)

1. Create your own Telegram bot by following [BotFather](https://t.me/BotFather) instructions
2. Copy the `API_KEY` (keep this key secret)

### Running the Bot

1. Copy this repository

```
git clone https://github.com/jloh02/capt-laundry-bot
```

2. Create a `.env` file in root folder with the following content and update Telegram bot API key

```
TELEGRAM_BOT_API_KEY=<YOUR_API_KEY>
```

3. Install Packages

```
pip install -r requirements.txt
```

4. Run Bot

```
python src/main.py
```

### Testing Deployment Configurations

Ensure you have docker installed

```
docker compose build
docker compose up -d
```

## Design Considerations

Instead of a DB, we opted for a local JSON file to allow for ease of deployment and logetivity of the project as this project will be managed at an individual basis outside of the management of CAPT
