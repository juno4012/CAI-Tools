import httpx
from ..core.config import settings


async def generate_ai_response(prompt: str) -> str:
    if settings.OPENAI_API_KEY:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=20
            )
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    return "AI not configured."