# TELEGRAM QUIZ BOT

Telegram quiz bot is created using the `python-telegram-bot` library. It allows you to create a bot which users can interact with to get random questions from [opentdb](https://opentdb.com/api_config.php) api.

![](https://github.com/msenior85/telegram-quiz-bot/actions/workflows/tests.yml/badge.svg)

## Features

Get and answer questions from the vast [opentdb](https://opentdb.com/) database via a telegram bot

## Getting Started

To use the bot, you'll need to follow these steps:

### Prerequisites

- `python >= 3.9`
- `python-telegram-bot >= v20`

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/msenior85/telegram-quiz-bot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd telegram-quiz-bot
    ```

3. Create virtual environment:

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment as per your operating system guidelines and install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Obtain a Telegram Bot Token from [@BotFather](https://t.me/BotFather) on Telegram.

2. Create a `.env` file in the project root and add your token:

    ```env
    BOT_TOKEN=your_bot_token_here
    ```

### Usage

Start the bot using the following command:

```bash
python run.py
```

### Contributing

If you'd like to contribute to the project, please follow the standard GitHub fork and pull request workflow.

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/msenior85/telegram-quiz-bot/blob/main/LICENSE) file for details.
