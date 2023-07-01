# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key


system_prompt = """
あなたは優秀な社内システムエンジニアです。
社員はWindows10のPCを利用しています。
ITリテラシーが低い社員からPCに関する質問やトラブルに対し、優しい言葉で回答します。
あなたの役割はシステムエンジニアであるため、例えば以下のようなPC以外ことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 「パソコンに関する質問」に回答するチャットボット")
st.image("22_win10.png")
st.write("どのような質問でしょうか？")
st.write("")
st.write("　　（入力例）OneDriveで同期エラーが発生してしまいました")
st.write("　　（入力例）XLOOKUPの具体的な使い方を教えてほしい")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
