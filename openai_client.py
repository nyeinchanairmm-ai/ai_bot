import openai
import os
# from db import session, ChatHistory
# from db import get_db_connection
from db import init_db, ChatHistory


# API Key (Env var မှာထားသင့်)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_bot_response(user_message: str) -> str:
    try:
        # OpenAI Chat API ကို အသုံးပြု
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",   # သုံးနိုင်သည့် model → gpt-4o-mini / gpt-4.1 / gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.7
        )

        # AI Response ကို ထုတ်ယူ
        answer = response["choices"][0]["message"]["content"].strip()

        # Database မှာ သိမ်းဆည်း
        chat_record = ChatHistory(user_message=user_message, bot_response=answer)
        init_db.add(chat_record)
        init_db.commit()

        return answer

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
