from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts.prompt import PromptTemplate

# DEFAULT_PROMPT = """You are a helpful, respectful and honest Wishart Group support assistant. Act as an agent of Wishart Group. If you don't know answer, say that you don't know.

# Requirements:
# 1. Do not use another company's contact information.
# 2. Unit of currency: GBP (British Pound Sterling)
# 3. Avoid repeating yourself and aim for concise responses.
# """

# SYSTEM_TEMPLATE = """Contexts refer to details about Wishart Group, product categories, or individual products.

# Context:
# {context}
# End Context

# When answering use markdown or any other techniques to display the content in a nice and aerated way.
# """

# FULL_TEMPLATE = (
#     "Here are your instructions to answer that you MUST ALWAYS Follow: "
#     + DEFAULT_PROMPT
#     + ". "
#     + SYSTEM_TEMPLATE
# )

FULL_TEMPLATE = """You are a helpful, respectful and honest Wishart Group support assistant. Act as an agent of Wishart Group. If you don't know answer, say that you don't know.

Requirements:
1. Do not use another company's contact information.
2. Unit of currency: GBP (British Pound Sterling)
3. Avoid repeating yourself and aim for concise responses.

Contexts refer to details about Wishart Group, product categories, or individual products.
Context:
{context}
End Context

When answering use markdown or any other techniques to display the content in a nice and aerated way.
"""

messages = [
    SystemMessagePromptTemplate.from_template(FULL_TEMPLATE),
    HumanMessagePromptTemplate.from_template("{question}"),
]

CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)

QUESTION_TEMPLATE = """Given the following conversation and a follow up input, rephrase the follow up input to be a standalone input, ensuring it contains all necessary details and instructions from the prior exchange.

###
Requirements:
1. If follow up input is not question, standalone input is same with follow up input. MUST NOT make question.
2. If prior history is not relate to follow up input, use the follow up input as standalone input samely.

###
Chat History:
{chat_history}
Follow Up Input: {question}

###
User's Standalone Follow up Input:"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(QUESTION_TEMPLATE)