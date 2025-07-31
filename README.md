# Yeab Game Zone - Telegram Ludo Bot

This is a production-ready Telegram bot for playing real-money Ludo games between two players. It integrates with the Chapa payment gateway for deposits and withdrawals and is designed for deployment on Render.

## Features

- **Two-Player Ludo:** Real-time, turn-based Ludo games.
- **Custom Win Conditions:** Win by getting 1, 2, or all 4 tokens home.
- **Emoji-Based Board:** Dynamic and clear in-chat game board representation that edits itself to prevent spam.
- **Real-Money Stakes:** Players stake real money, with a 10% commission on the pot.
- **Chapa Integration:** Secure deposits via Chapa payment gateway.
- **Withdrawal System:** Request withdrawals to Telebirr or CBE bank accounts.
- **Network Dispute Resolution:** Automatic forfeiture for inactive players (after a 90-second warning period).
- **Cloud-Native:** Designed for seamless deployment on the Render PaaS with a `render.yaml` blueprint.

## Development Setup (GitHub Codespaces)

1.  Click the "Code" button on the GitHub repository page.
2.  Select the "Codespaces" tab.
3.  Click "Create codespace on main".
4.  The environment will automatically build, install dependencies, initialize the database, and start the PostgreSQL service.
5.  Create a `.env` file in the root directory by copying `.env.example`.
6.  Fill in the values in your new `.env` file. You will need a test Telegram bot token and a Chapa test key.
7.  Run the application locally using the command: `python main.py`
8.  To make the local webhook work, you'll need a tool like `ngrok` to expose your port 8000 to the internet. Update `WEBHOOK_URL` in your `.env` file with the `ngrok` URL.

## Deployment to Render

1.  **Fork this repository** to your own GitHub account.
2.  Go to your [Render Dashboard](https://dashboard.render.com/) and click **"New" -> "Blueprint"**.
3.  Connect the forked GitHub repository.
4.  Render will automatically detect the `render.yaml` file. Give your services a unique name prefix.
5.  Under the **Environment** section for the `yeab-game-zone-api` service, you must add the following secret environment variables:
    -   `TELEGRAM_BOT_TOKEN`: Your bot's token from BotFather.
    -   `CHAPA_API_KEY`: Your secret API key from the Chapa dashboard.
6.  Click **"Apply"**. Render will provision the PostgreSQL database, build the web service and worker, run the `initdb` command, and start the application.
7.  The first deployment will automatically set the Telegram webhook to your new Render URL. Your bot is now live.

## Key Environment Variables

-   `TELEGRAM_BOT_TOKEN`: **(Secret)** Your Telegram Bot's API token.
-   `CHAPA_API_KEY`: **(Secret)** Your Chapa API V1 secret key.
-   `DATABASE_URL`: **(Provided by Render)** The connection string for your PostgreSQL database.
-   `WEBHOOK_URL`: **(Provided by Render)** The public URL of the FastAPI web service.