import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['LEPQ+PdKPSLcoS9GBbdFukdoHl+KigQAE1/6atOcvQn97Own17jB19NydaKRrEuMNR0c0P2h9jFk7IVWb3DQs/cEJGvVFGF6Ki/v+Nw8+QWGTYpeEkk9v7Yb6/OCR0OS7RmAlJWhRW42/a6 kmbQiMgdB04t89/1O/w1cDnyilFU='])
handler = WebhookHandler(os.environ['1268eb4f16e5d543a622a4c4341abbd6'])

import openai

openai.api_key = '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'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    if not body:
        abort(400)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK',200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 使用ChatGPT進行回應生成
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Hi."},
            {"role": "user", "content": user_message}
        ]
    )

    # 從回應物件中取得ChatGPT生成的回應
    chat_reply = response.choices[0].message.content

    # 回傳ChatGPT生成的回應給LINE BOT的用戶
    message = TextSendMessage(text=chat_reply)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    