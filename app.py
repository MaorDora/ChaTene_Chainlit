import chainlit as cl
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    model = None
else:
    genai.configure(api_key=api_key)
    system_instruction = """
    אתה ChaTene, עוזר לוגיסטי חכם למערך הטנ"א בצה"ל.
    המטרה שלך: לספק מידע על מלאי, הזמנות וסטטוס טיפולים.
    חוקים:
    1. תענה אך ורק על סמך המידע שמוצג לך. אל תמציא מק"טים או נתונים (Zero Hallucinations).
    2. אם המידע לא קיים, תגיד: "לא נמצאו נתונים במערכת".
    3. דבר בעברית רשמית וקצרה (שפה צבאית/טכנית).
    4. בסוף כל תשובה המכילה מידע, ציין את המקור (למשל: "מקור: SAP Module MM").
    """
    # שימוש במודל פשוט יותר למקרה שהשם החדש עושה בעיות
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)

@cl.on_chat_start
async def start():
    await cl.Message(content="שלום! אני ChaTene (גרסה בסיסית). איך אפשר לעזור?").send()

@cl.on_message
async def main(message: cl.Message):
    if not model:
        await cl.Message(content="שגיאה: חסר API Key").send()
        return

    try:
        response = await model.generate_content_async(message.content)
        await cl.Message(content=response.text).send()
    except Exception as e:
        await cl.Message(content=f"שגיאה: {str(e)}").send()