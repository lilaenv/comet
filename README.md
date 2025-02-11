# Comet - Your special AI assitant

[![CodeQL](https://github.com/lilaenv/comet/actions/workflows/codeql.yml/badge.svg)](https://github.com/lilaenv/comet/actions/workflows/codeql.yml)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD-orange.svg?style=flat)](https://github.com/lilaenv/comet/blob/main/LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.12-blue.svg?style=flat)

**Comet** is your AI assistant that runs in Discord.

## Getting Started

Follow the steps below to set up the application on your local environment.

### Prerequisites

1. **Set up Python environment**

    We recommend **uv** to set up python environment and manage dependencies. Please follow the [official documentation](https://docs.astral.sh/uv/) to install uv.

2. **Clone repository and install dependencies**

    ```
    # ------ clone repository ------
    git clone https://github.com/lilaenv/comet.git

    # ------ install dependencies ------
    # with uv
    uv sync

    # without uv
    pip install -r requirements.txt
    ```

3. **Prepare .env file**

    This application requires a `.env` file for configuration. Follow these steps:
    - Copy the `.env.example` file and rename it to `.env`.
    - Fill in the actual values.

4. **Setup OpenAI API access**

    Follow the steps below to get your OpenAI API key:
    - Create an account on [OpenAI developer platform](https://platform.openai.com/docs/overview).
    - Go to the API keys section of your account settings and generate a new API key.
    - Keep this key safe and add it to your `.env` file under the variable `OPENAI_API_KEY`.

### Create and invite Discord application

1. Go to [Discord Developer Portal](https://discord.com/developers/bots), create a new discord bot.

2. Go to the Bot tab and
   - Click "**Reset Token**" and keep it safe and add it to your `.env` file under the variable `DISCORD_BOT_TOKEN`.
   - Enable "**SERVER MEMBERS INTENT**" and "**MESSAGE CONTENT INTENT**".

3. Go to the OAuth2 tab and generate an invite link for your bot by picking follow scopes and permissions.

    **SCOPES**
    - application commands
    - bot

    **BOT PERMISSIONS**
    - View Channels
    - Send Messages
    - Create Public Threads
    - Send Messages in Threads
    - Manage Messages
    - Manage Threads
    - Read Message History
    - Use Slash Commands

4. Invite the bot to your guild using the generated url.

### Write a system prompt

> [!IMPORTANT]
> When using an bot on large-scale or open servers, it is highly recommended to craft a detailed and robust system prompt.

Make a copy of `.prompt.example.yml` and rename it to `.prompt.yml`. Then, edit the `system_prompt` values.

Example:

```yaml
system_prompt: |
  You are a helpful assistant that strictly follows the [System Instructions].

  # [System Instructions]

  Detail instructions...
```

### Run the bot

Finally, make sure all values in the .env file are filled in correctly, and then execute the following.
```
python -m src.comet [--log <log_level>]
```
**Note:** The `--log <log_level>` option is optional. If it is not specified, the default log level is `INFO`. The available log levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.


## Commands

Here are all commands available in Discord. **But some commands require specific roles or permissions to execute**.

### Support Commands

Use these commands to get help or learn about the application.

<table>
  <tr>
    <th>Command</th>
    <th>Description</th>
    <th>Status</th>
  </tr>
  <tr>
    <td><code>/help</code></td>
    <td>Displays the list of available commands.</td>
    <td>Planned</td>
  </tr>
  <tr>
    <td><code>/info</code></td>
    <td>Shows information about the application.</td>
    <td>Planned</td>
  </tr>
</table>

### Chat Commands

<table>
  <tr>
    <th>Command</th>
    <th>Description</th>
    <th>Status</th>
  </tr>
  <tr>
    <td><code>/chat</code></td>
    <td>Create thread and start chat with openai model.</td>
    <td>Implemented</td>
  </tr>
  <tr>
    <td><code>/limit</code></td>
    <td>Limit the number of API requests.</td>
    <td>Planned</td>
  </tr>
</table>

### User Management Commands

Manage user access permissions by adding or removing the status of permission in the database.

<table>
  <tr>
    <th>Command</th>
    <th>Description</th>
    <th>Status</th>
  </tr>
  <tr>
    <td><code>/add_access</code></td>
    <td>Add a access type for a user.</td>
    <td>Implemented</td>
  </tr>
  <tr>
    <td><code>/check_access</code></td>
    <td>Check the user's access type.</td>
    <td>Implemented</td>
  </tr>
  <tr>
    <td><code>/rm_access</code></td>
    <td>Remove a access type from a user.</td>
    <td>Implemented</td>
  </tr>
</table>