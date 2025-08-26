import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_bot_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

    """
    Dummy bot response for testing (no API call).
    """
    # အလွယ်တကူ sample response ပေး
    responses = [
        "Hello! I'm a dummy bot 🤖",
        "You said: " + user_message,
        "This is just a test response 🚀",
        "Everything is working fine ✅"
    ]
    
    # တစ်ခါလုံး random တစ်ခု ပြန်ပေး
    import random
    return random.choice(responses)