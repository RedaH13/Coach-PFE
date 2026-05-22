from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class CoachState(TypedDict):
    # add_messages empiler l'historique auto
    messages: Annotated[Sequence[BaseMessage], add_messages]
    chat_id: str
    user_id: str
    timestamp: int