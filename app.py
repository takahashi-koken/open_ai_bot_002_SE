# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key


system_prompt = """
あなたは優秀な社内システムエンジニアです。
社員はWindows10のPCとAndroidのスマホを利用しています。
ITリテラシーの低い社員からPCやスマホに関する質問やトラブルに対し、
優しい言葉で箇条書きで簡潔に回答してください。
あなたの役割はシステムエンジニアであるため、
例えば以下のようなPC以外ことを聞かれても、絶対に答えないでください。



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


#---------------------------------------------
# ユーザーインターフェイスの構築
#---------------------------------------------
#タイトル
st.title("PCやスマホに関する質問に回答します")

#見出し
lines = [
    "①新しい相談は[F5]押下等でリロードしてください     ",
    "②入力後は [Ctrl]＋[Enter] で実行します"
]
text = "\n".join(lines)
st.write(text)

#画像
st.image("22_win10.png")


# Shift + Enter でテキスト欄の行数を増やす
script = """
document.addEventListener("keydown", function(e) {
    if (e.shiftKey && e.keyCode === 13) {
        let textarea = document.querySelector("textarea");
        textarea.rows += 1;
    }
});
"""

#テキスト入力
st.write("どのような質問でしょうか")

#例示
lines = [
    "　　（入力例）OneDriveで同期エラーが発生してしまった    ",
    "　　（入力例）Excel関数「XLOOKUP」の具体的な使い方を教えてほしい  ",
    "　　（入力例）ChatGPTはインストール済み。ChatGPTでのQAの作成方法を教えて  ",
    "　　（入力例）スマホの写真画像を削除する方法を教えて  "
]
text = "\n".join(lines)
st.write(text)

#テキスト入力
user_input = st.text_area("メッセージを入力してください。入力後は [Ctrl]＋[Enter] ", key="user_input" , on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

st.write(f"<script>{script}</script>", unsafe_allow_html=True)

