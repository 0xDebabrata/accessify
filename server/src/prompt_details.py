from pydantic import BaseModel, Field


class PromptDetails(BaseModel):
    sysMessage: str
    userMessage: str
    temperature: float = Field(ge=0, le=1)
