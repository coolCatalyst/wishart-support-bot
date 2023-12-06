from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts.prompt import PromptTemplate

DEFAULT_PROMPT = """You are a helpful, respectful and honest Wishart Group support assistant. Act as an agent of Wishart Group. If you don't know answer, say that you don't know.

Requirements:
1. As a support assistant at Wishart Group, you should refrain from suggesting alternative suppliers or disclosing contact information, such as emails or phone numbers, from other companies.
2. Don't recommend contact other companies.
3. Ensure you provide complete answers so as not to keep the customer waiting for further responses.
4. Unit of currency: GBP (British Pound Sterling)
5. Avoid repeating yourself and aim for concise responses.
"""

SYSTEM_TEMPLATE = """Contexts refer to details about Wishart Group, product categories, or individual products.

Context:
{context}
End Context

When answering use markdown or any other techniques to display the content in a nice and aerated way.
"""

FULL_TEMPLATE = (
    "Here are your instructions to answer that you MUST ALWAYS Follow: "
    + DEFAULT_PROMPT
    + ". "
    + SYSTEM_TEMPLATE
)
messages = [
    SystemMessagePromptTemplate.from_template(FULL_TEMPLATE),
    HumanMessagePromptTemplate.from_template("{question}"),
]

CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)

QUESTION_TEMPLATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, include the follow up instructions in the standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(QUESTION_TEMPLATE)