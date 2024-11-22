from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext
from flask import Flask
from threading import Thread

# 환영 메시지 처리 함수
async def welcome_new_member(update: Update, context: CallbackContext) -> None:
    for new_user in update.message.new_chat_members:
        user_name = new_user.first_name
        welcome_message = (
            f"{user_name}님!\n"
            "한국을 알고 싶뉘?\n"
            "너구리를 사랑 하뉘?\n"
            "돈도 벌고 싶뉘?\n"
            "부자가 되고 싶뉘?\n\n"
            "이거이 구리토큰이고! 너츠토큰이야!"
        )
        await update.message.reply_text(welcome_message)

# 기본 시작 명령어
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("안녕하세요! 환영 메시지 봇입니다. 😊")

# Flask 서버 생성
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 메인 실행 함수
# 메인 실행 함수
def main():
    import os  # 환경 변수를 읽기 위한 모듈 추가

    # 환경 변수에서 API 키 읽기
    BOT_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    
    if not BOT_TOKEN:
        raise ValueError("환경 변수 TELEGRAM_API_TOKEN이 설정되지 않았습니다.")

    
    # Application 객체 생성
    application = Application.builder().token(BOT_TOKEN).build()

    # 명령어 및 핸들러 추가
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    # Flask 서버를 별도 스레드에서 실행
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # 봇 실행
    print("봇이 실행 중입니다...")
    application.run_polling()

if __name__ == "__main__":
    main()
