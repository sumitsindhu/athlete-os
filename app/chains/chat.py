from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable


def build_chat_chain_from_model(model: BaseChatModel) -> Runnable:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Reply concisely."),
            ("human", "{message}"),
        ]
    )
    return prompt | model
