from django.conf import settings
from openai import OpenAI

client = OpenAI(
    base_url="https://models.github.ai/inference", api_key=settings.OPENAI_API_KEY
)


def translate_text(text, target_language):
    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a translator. Translate the following text to {target_language}. Preserve the formatting.",
                },
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Translation error: {str(e)}"
