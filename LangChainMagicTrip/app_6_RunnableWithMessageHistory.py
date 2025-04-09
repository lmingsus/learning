'''
https://python.langchain.com/api_reference/core/runnables/langchain_core.runnables.history.RunnableWithMessageHistory.html
Example: Chat message history with an in-memory implementation for testing.
'''

# Example: Chat message history with an in-memory implementation for testing.

from operator import itemgetter
from typing import List

from langchain_openai.chat_models import ChatOpenAI

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.runnables import (
    RunnableLambda,
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
from langchain_core.runnables.history import RunnableWithMessageHistory


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history.
    - **BaseChatMessageHistory**: 提供聊天歷史記錄的基本介面
    - **BaseModel**: 來自 Pydantic，提供資料驗證功能
    """

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

# Here we use a global variable to store the chat message history.
# This will make it easier to inspect it to see the underlying results.
store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


history = get_by_session_id("1")
history.add_message(AIMessage(content="hello"))
print(store)  # noqa: T201

# ===============================================================
# Example where the wrapped Runnable takes a dictionary input:
from typing import Optional

from langchain_community.chat_models import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory


prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an assistant who's good at {ability}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | ChatAnthropic(model="claude-2")

chain_with_history = RunnableWithMessageHistory(
    chain,
    # Uses the get_by_session_id function defined in the example
    # above.
    get_by_session_id,
    input_messages_key="question",
    history_messages_key="history",
)

print(chain_with_history.invoke(  # noqa: T201
    {"ability": "math", "question": "What does cosine mean?"},
    config={"configurable": {"session_id": "foo"}}
))

# Uses the store defined in the example above.
print(store)  # noqa: T201

print(chain_with_history.invoke(  # noqa: T201
    {"ability": "math", "question": "What's its inverse"},
    config={"configurable": {"session_id": "foo"}}
))

print(store)  # noqa: T201



# ===============================================================
# Example where the session factory takes two keys, user_id and conversation id):
store = {}

def get_session_history(
    user_id: str, conversation_id: str
) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = InMemoryHistory()
    return store[(user_id, conversation_id)]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an assistant who's good at {ability}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | ChatAnthropic(model="claude-2")

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)

with_message_history.invoke(
    {"ability": "math", "question": "What does cosine mean?"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}}
)