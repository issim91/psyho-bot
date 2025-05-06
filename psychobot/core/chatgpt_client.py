from openai import AsyncOpenAI
from typing import List, Dict
from psychobot.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS


class ChatGPTClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens = OPENAI_MAX_TOKENS

    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Извините, произошла ошибка при обработке вашего сообщения. Пожалуйста, попробуйте еще раз."

    async def summarize_session(self, messages: List[Dict[str, str]]) -> str:
        summary_prompt = {
            "role": "system",
            "content": "Пожалуйста, составьте краткое резюме психологической сессии, выделив основные темы, проблемы и рекомендации."
        }
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[summary_prompt] + messages,
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None 
