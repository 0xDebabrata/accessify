import requests
from typing import List
from config import get_config
from .system_prompts import prompts
from .enum_types import ElementType, RoleType
from .bearer_auth import BearerAuth


async def connectGPT(elementList: List[str], type: ElementType):
    config = get_config()

    # each element of the elementList is an url
    gptInputString: str = "\n".join(elementList)

    payload = {
        "model": "gpt-3.5-turbo",
        "temperature": prompts[type].temperature,
        "messages": [
            {
                "role": RoleType.SYSTEM,
                "content": prompts[type].sysMessage,
            },
            {
                "role": RoleType.USER,
                "content": prompts[type].userMessage + gptInputString,
            },
        ],
        "max_tokens": 2000,
    }

    # we are using json hence content type is already set
    # bearer token is already set using the auth parameter,
    # hence header is commented
    headers = {
        # "Content-Type": "application/json",
        # "Authorization": f"Bearer {config.OPENAI_API_KEY}",
    }

    response = requests.post(
        config.OPENAI_PROCESSING_URL,
        headers=headers,
        json=payload,
        auth=BearerAuth(config.OPENAI_API_KEY),
    )

    json_data = response.json()
    response = json_data.choices[0].message.content

    return response
