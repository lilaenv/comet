# Comet

[![CodeQL](https://github.com/lilaenv/comet/actions/workflows/codeql.yml/badge.svg)](https://github.com/lilaenv/comet/actions/workflows/codeql.yml)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD-orange.svg?style=flat)](https://github.com/lilaenv/comet/blob/main/LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.12-blue.svg?style=flat)

**Comet** は Discord 上で動作する AI アシスタントです。

## Getting Started

ここではローカル環境に Comet の動作環境を構築します。

### 事前準備

1. **Python 環境の構築**

    **uv** の利用を推奨しています。インストール方法は[公式ドキュメント](https://docs.astral.sh/uv/)を参照してください。

2. **リポジトリをクローンし、依存関係をインストールする**

    ```
    # ------ clone repository ------
    git clone https://github.com/lilaenv/comet.git

    # ------ install dependencies ------
    # with uv
    uv sync

    # without uv
    pip install -r requirements.txt
    ```

3. **.env ファイルの準備**

    bot の設定に `.env` ファイルを利用します。以下の手順に従ってください。
    - `.env.example` ファイルをコピーし、それを `.env` に改名する。
    - 各値に、実際の値を入力する。

4. **OpenAIのAPIキーを準備**

    以下の手順に従ってください。
    - [OpenAI developer platform](https://platform.openai.com/docs/overview) でアカウントを作成する。
    - API キーを作成し、その値を `.env` の変数 `OPENAI_API_KEY` に追加する。
    - クレジットを追加する。

5. **AnthropicのAPIキーを取得**

    以下の手順に従ってください。
    - [Console Account](https://console.anthropic.com/login) にログイン。
    - API キーを作成し、その値を `.env` の変数 `ANTHROPIC_API_KEY` に追加する。
    - クレジットを追加する。

### Discord application を作成しサーバーに招待**

1. [Discord Developer Portal](https://discord.com/developers/bots) で新しい application を作成してください。

2. Bot タブ内で以下の操作を行ってください:
    - **Reset Token** をクリックし、表示されたトークンを `.env` の変数 `DISCORD_BOT_TOKEN` に追加する。
    - **SERVER MEMBERS INTENT** と **MESSAGE CONTENT INTENT** を有効にする。

3. Ouath2 タブに移動し、scopes と permissions を選択して bot の招待 URL を作成します:

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

4. 生成された URL で bot をサーバーに招待します。

### システムプロンプトを書く

>[!IMPORTANT]
> 中規模以上のサーバーやオープンなサーバーで利用する場合、詳細かつ堅牢なシステムプロンプトを記述することを強く推奨します。システムプロンプトが不十分な場合、インジェクション攻撃などの対象となるリスクがあります。

`.prompt.example.yml` をコピーして `.prompt.yml` に改名し、その中の `system_prompt` に記述してください。

Example:

```yaml
system_prompt: |
    あなたは [システム指示] に厳密に従うAIアシスタントです。

    # [システム指示]

    **システム指示の詳細**
    - Markdown形式が利用できます。

    詳細な指示...
```

### Bot を動作させる

.envファイルと .prompt.yml のすべての値が正しく入力されていることを確認し、以下のコマンドを実行してください。
```
python -m src.comet [--log <log_level>]
```

**Note:**　`--log <log_level>` はオプションです。通常の利用では入力する必要はありません。log_level に選択可能な値は `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` です。デフォルトは `INFO` です。


## コマンド一覧

Discord 上で利用可能なコマンド一覧です。一部のコマンドは特別な権限が必要です。

### サポートコマンド

<table>
    <tr>
        <th>Command</th>
        <th>Description</th>
        <th>Status</th>
    </tr>
    <tr>
        <td><code>/help</code></td>
        <td>利用可能なすべてのコマンドを表示します</td>
        <td>計画中</td>
    </tr>
    <tr>
        <td><code>/info</code></td>
        <td>Botのガイドを表示します</td>
        <td>計画中</td>
    </tr>
</table>

### チャットコマンド

<table>
    <tr>
        <th>Command</th>
        <th>Description</th>
        <th>Status</th>
    </tr>
    <tr>
        <td><code>/gpt</code></td>
        <td>gpt モデルを利用してチャットを開始します</td>
        <td>実装済</td>
    </tr>
    <tr>
        <td><code>/claude</code></td>
        <td>claude モデルを利用してチャットを開始します</td>
        <td>実装済</td>
    </tr>
    <tr>
        <td><code>/limit</code></td>
        <td>API へのリクエスト回数を制限します</td>
        <td>計画中</td>
    </tr>
</table>

### アクセス管理コマンド

<table>
    <tr>
        <th>Command</th>
        <th>Description</th>
        <th>Status</th>
    </tr>
    <tr>
        <td><code>/add_access</code></td>
        <td>ユーザーにアクセスタイプを付与します</td>
        <td>実装済</td>
    </tr>
    <tr>
        <td><code>/check_access</code></td>
        <td>ユーザーのアクセスタイプを確認します</td>
        <td>実装済</td>
    </tr>
    <tr>
        <td><code>/rm_access</code></td>
        <td>ユーザーからアクセスタイプを削除します</td>
        <td>実装済</td>
    </tr>
</table>

## Contributing

バグを発見したり、新機能を提案したい場合は、[CONTRIBUTING-JP.md](https://github.com/lilaenv/comet/blob/main/CONTRIBUTING-JP.md)を参照してください。
