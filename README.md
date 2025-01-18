# Gemini Recipe
Gemini APIで簡単に遊べるプロジェクトです！

## 準備

### Gemini APIキーの作成
公式Geminiサイトや以下のチュートリアルを参考にAPIキーを作成してください。

[Gemini APIキーの作成方法](https://tech-useit-wealth.com/gemini-api-tutorial)

APIキーを作成したら、プロジェクトディレクトリに`.env`ファイルを作成し、以下のように記載します。

```
GOOGLE_API_KEY="your API key"
```

### Dockerの設定
このプロジェクトはDocker環境で簡単に動作するように設計されています。

#### Dockerイメージのビルド
まず、Dockerイメージをビルドします。この手順は、`Dockerfile`を変更しない限り1回だけ実行すれば十分です。

```
docker build -t gemini_recipe .
```

#### Dockerコンテナの起動
イメージのビルドが完了したら、以下のコマンドでコンテナを作成・起動します。

```
docker compose up -d
```

コンテナのシェルにアクセスするには、以下を実行してください。

```
docker exec -it gemini_recipe bash
```

ここから、必要に応じてPythonスクリプトを実行できます（詳細は後述）。

#### Dockerの終了
コンテナシェルを終了するには以下を実行します。

```
exit
```

コンテナを停止するには以下を実行します。

```
docker compose down
```

## Pythonスクリプトの実行

### Streamlitアプリケーション
`gemini_agent.py`はStreamlitアプリです。以下のコマンドで起動します。

```
streamlit run gemini_agent.py
```

### その他のスクリプト
その他のPythonスクリプトは以下のコマンドで実行できます。

```
python script_name.py
```

`script_name.py`を実行したいスクリプト名に置き換えてください。
