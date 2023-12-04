from typing import List, Tuple
from pydantic import BaseModel

# Pydantic model for the chat history input
class ChatHistory(BaseModel):
    history: List[Tuple[str, str]]
    
class ChatMessage(BaseModel):
    message: str