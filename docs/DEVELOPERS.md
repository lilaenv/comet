# 開発者向けドキュメント

Comet の開発者、またはソースコードの改良に携わる貢献者に向けたドキュメントです。開発またはソースコードに関する貢献を行う場合は、以下のルールを遵守していただくようお願いいたします。

## 重要事項

以下のことを念頭に置いて作業してください。特に、コミット前に確認してください。
- コミットは[テンプレート](https://github.com/lilaenv/comet/blob/main/.github/.gitmessage)に従って作成してください。
- プルリクエストは[テンプレート](https://github.com/lilaenv/comet/blob/main/.github/PULL_REQUEST_TEMPLATE.md)に従って作成してください。

## 開発環境

ここでは、macOS のユーザーが comet の開発環境を構築するケースを想定します。

### エディタの準備

**VSCode** または **Cursor** を推奨しています。ただし、同様の環境を準備できればどのようなエディタでも構いません。以下は VSCode を利用する場合の拡張機能の紹介です。Cursor にも対応しています。

- 必須機能
    - [Mypy Type Checker](https://github.com/microsoft/vscode-mypy)
    - [Python](https://github.com/Microsoft/vscode-python)
    - [Ruff](https://github.com/astral-sh/ruff-vscode)
    - [SQLite Viewer](https://github.com/qwtel/sqlite-viewer-vscode)

- 必要に応じて
    - [Gihub Actions](https://github.com/github/vscode-github-actions)
    - [Github Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
    - [IntelliCode](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode)
    - [Jupyter](https://github.com/Microsoft/vscode-jupyter)
    - [YAML](https://github.com/redhat-developer/vscode-yaml)

ChatGPT の MacOS app を利用している方は [OpenAI work with Apps](https://help.openai.com/en/articles/10128592-how-to-install-the-work-with-apps-visual-studio-code-extension)
もおすすめです。

vscode の基本的な設定は [settings.json](https://github.com/lilaenv/comet/blob/main/.vscode/settings.json) を参考にして下さい。

AI の利用は特に規制はしていません。Copilot, Claude, gpt など利用は自由です。ただし、AI の出力をそのままコピペするのではなく、それが本当に正しく動作するか、命名規則に即しているかなど確認をしてからコミットしてください。

### python の準備

**uv** を採用しています。python のインストールからパッケージまで一括して管理できます。インストール方法などの詳細は[公式サイト](https://docs.astral.sh/uv/)を参照してください。

以下は、基本的な uv コマンドの一覧です。

<table>
    <tr>
        <th>コマンド</th>
        <th>説明</th>
    </tr>
    <tr>
        <td>uv init [project]</td>
        <td>プロジェクトの作成</td>
    </tr>
    <tr>
        <td>uv init [project] -p 3.12</td>
        <td>python のバージョンを指定してプロジェクトを作成</td>
    </tr>
    <tr>
        <td>uv sync</td>
        <td>依存関係を同期</td>
    </tr>
    <tr>
        <td>uv add [package]</td>
        <td>依存関係を追加</td>
    </tr>
    <tr>
        <td>uv remove [package]</td>
        <td>依存関係を削除</td>
    </tr>
    <tr>
        <td>uv --version</td>
        <td>uv のバージョンを確認</td>
    </tr>
    <tr>
        <td>uv self update</td>
        <td>uv を最新バージョンに更新</td>
    </tr>
</table>

## リポジトリのフォークまたはクローン


## コーディング規則

[PEP8](https://pep8-ja.readthedocs.io/ja/latest/) に従います。さらに、コード品質の向上とバグの事前防止を目的として mypy と ruff を採用しています。

基本的に、mypy と ruff の警告が出ないようにコーディングすれば、コーディング規約を満たしています。ただし、以下に例外を示します。例外の内容は警告されないので注意してください。

- Docstring とコメントは72文字以内で記述してください。
- インラインコメントは終点が99文字に収まるように記述してください。
- 特定の文脈においては、ワイルドカードインポートの使用を許可しています。ワイルドカードインポートを使用する際は、直前にその理由を記述してください。ただし、以下の Exception に該当する場合は理由を記述する必要はありません。

    **Note**

    ただし、新たに無条件にワイルドカードインポートの使用を許可する事態に直面した場合は、Issue にて報告してください。

    Example:
    ```python
    # ここに理由を記述
    from hogehoge import *
    ```

    Exception:
    - `commands` ディレクトリ内における `access_control` のワイルドカードインポート
    - `commands` ディレクトリ内における直接菅家のある `services` ディレクトリ内のモジュールのインポート
    - `__main__.py` における `from .commands import *`

**Note**

`commands` ディレクトリ内おけるワイルドカードインポートについて、たとえば `from src.comet.utils.access_control import *` を通常のインポート `eg., from path/to/access_control import function`にすると動かないのですが理由がわかりません。

長期にわたって放置してしまい萎えています。もしリファクタリングしてもいいよという寛大な方がおられましたらお願いします。


## ブランチ構成

[A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) を採用しています。ただし、master は main に名称を変更しています。

![ブランチ全体図](https://github.com/lilaenv/comet/blob/main/images/branch.png?raw=true)

各ブランチについて詳しく説明します

<table>
    <tr>
        <th>ブランチ名</th>
        <th>説明</th>
    </tr>
    <tr>
        <td>main</td>
        <td>原則として直接の作業は行わない</td>
    </tr>
    <tr>
        <td>hotfix</td>
        <td>リリース後の緊急を要する修正を行う<br>hotfix / [ id ] という名で main から派生させる<br>作業完了後は main develop へ PR を作成してマージ</td>
    </tr>
    <tr>
        <td>release</td>
        <td>リリース前の動作確認を行う<br>このブランチに新規機能は追加しない<br>作業完了後は main へ PR を作成してマージ & タグ付け<br>バグ修正や変更をコミットしたと場合は develop にも PR を作成してマージ</td>
    </tr>
    <tr>
        <td>develop</td>
        <td>開発のベースとなるブランチ<br>main から派生させる</td>
    </tr>
    <tr>
        <td>feature</td>
        <td>新機能の開発を行う<br>feature / [ id ] という名で develop から派生させる<br>作業完了後は develop へ PR を作成してマージ</td>
    </tr>
</table>

## Issue

ソースコードの改善について、Issue を作成して気軽に意見をお寄せください。もちろん、バグ報告や新機能の提案も歓迎しています。Issueの作成は[こちら](https://github.com/lilaenv/comet/issues)からお願いします。

## コミットルール

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) を参考にしています。また、[conventional-changelog-cli](https://github.com/conventional-changelog/conventional-changelog/tree/master/packages/conventional-changelog-cli) を利用して CHANGELOG の自動生成を行います。必ず下記のルールを遵守してください。

- コミットメッセージは[テンプレート](.github/.gitmessage)に従って作成してください。以下のコマンドでコミット時にテンプレートを表示することができます。ただし、`-m` オプションは使用しないでください。

    ```bash
    git config commit.template /path/to/.gitmessage
    ```

## Pull Request

Pull Request は必ず[テンプレート](.github/PULL_REQUEST_TEMPLATE.md)に従って作成してください。
