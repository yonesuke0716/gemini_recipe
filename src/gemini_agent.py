import os
from io import StringIO
import sys

import pandas as pd
import duckdb
import streamlit as st
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import GoogleGenerativeAI
from pygwalker.api.streamlit import StreamlitRenderer


api_key = os.environ["GOOGLE_API_KEY"]


@st.cache_resource
def get_pyg_renderer(df: pd.DataFrame) -> str:
    renderer = StreamlitRenderer(df, kernel_computation=True)
    return renderer


# Streamlitページの幅を調整する
st.set_page_config(page_title="gemini_agent", layout="wide")

# === Streamlitアプリ ===
st.title("GeminiAgent_DataAnalyzer")
st.subheader("探索的データ分析")
st.sidebar.subheader("GeminiAgent")
# ログキャプチャ用のStringIOを設定
log_stream = StringIO()
sys.stdout = log_stream  # 標準出力をStringIOにリダイレクト

uploaded_file = st.sidebar.file_uploader(
    "CSVファイルをアップロードしてください", type="csv"
)
# ファイルがアップロードされている場合
if uploaded_file is not None:
    try:
        # CSVデータの読み込み
        df = duckdb.read_csv(uploaded_file).to_df()
        renderer = get_pyg_renderer(df)

        renderer.explorer()
        # 質問の入力
        user_question = st.sidebar.text_area(
            "お手伝いできることはありますか？",
            "データセットの概要を解説してください。",
            height=150,
        )
        # ユーザーが質問を入力した場合
        if st.sidebar.button("Agentの実行"):
            llm = GoogleGenerativeAI(
                model="gemini-1.5-flash", temperature=0, api_key=api_key
            )
            agent = create_pandas_dataframe_agent(
                llm,
                df,
                verbose=True,
                allow_dangerous_code=True,
            )
            if user_question.strip():
                st.sidebar.write("AIが回答を生成中です...")
                try:
                    # エージェントが質問を解析して回答
                    st.sidebar.success("AIの回答:")
                    st.sidebar.write(agent.invoke(user_question)["output"])
                    # ログを取得して表示
                    st.sidebar.subheader("Agentの思考Logs")
                    logs = log_stream.getvalue()
                    st.sidebar.text_area("Logs", logs, height=300)
                except Exception as e:
                    st.error(f"エージェント処理中にエラーが発生しました: {e}")
            else:
                st.warning("問題を入力してください。")
    except Exception as e:
        st.error(f"CSVの読み込み中にエラーが発生しました: {e}")
# 標準出力を元に戻す
sys.stdout = sys.__stdout__
st.write("---")
st.write(
    "このアプリでは、CSVデータに基づいて質問に答えるAIエージェントを利用しています。"
)
