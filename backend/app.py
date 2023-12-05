import asyncio
import dotenv
import gradio as gr
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores.pinecone import Pinecone
import logging
import os
import pinecone
from typing import Awaitable


dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV"),
)
index_name = os.getenv("PINECONE_INDEX_NAME")
index = pinecone.Index(index_name)

openai_api_key = os.getenv("OPENAI_API_KEY")
temperature = os.getenv("TEMPERATURE")
model = os.getenv("MODEL")

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = Pinecone(index, embeddings, "text")
retriever = vectorstore.as_retriever()


DEFAULT_PROMPT = """You are a helpful, respectful and honest Wishart Group support assistant. Act as an agent of Wishart Group. If you don't know answer, say that you don't know.

Requirements:
1. As a support assistant at Wishart Group, you should refrain from suggesting alternative suppliers or disclosing contact information, such as emails or phone numbers, from other companies.
2. Don't recommend contact other companies.
3. Ensure you provide complete answers so as not to keep the customer waiting for further responses.
4. Unit of currency: GBP (British Pound Sterling)
"""

def create_prompt_template():
    system_template = """Contexts refer to details about Wishart Group, product categories, or individual products.

Context:
{context}
End Context
"""
    full_template = (
        "Here are your instructions to answer that you MUST ALWAYS Follow: "
        + DEFAULT_PROMPT
        + ". "
        + system_template
    )
    messages = [
        SystemMessagePromptTemplate.from_template(full_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
    CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
    return CHAT_PROMPT


question_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, include the follow up instructions in the standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(question_template)

title = "Wishart support chatbot"
description = """
This is a chatbot that explain about wishart.
"""
css = """.toast-wrap { display: none !important } """

async def predict(message, history):
    output = ""
    
    callback = AsyncIteratorCallbackHandler()
    answering_llm_stream = ChatOpenAI(
        temperature=temperature,
        model=model,
        streaming=True,
        verbose=True,
        callbacks=[callback],
        openai_api_key=openai_api_key,
    )
    
    doc_chain_stream = load_qa_chain(
        answering_llm_stream, chain_type="stuff", prompt=create_prompt_template(), verbose=True
    )
    
    question_llm = ChatOpenAI(
        temperature=temperature,
        model=model,
        streaming=False,
        verbose=True,
        callbacks=None,
        openai_api_key=openai_api_key,
    )
    
    qa_stream = ConversationalRetrievalChain(
        retriever=retriever,
        question_generator=LLMChain(
            llm=question_llm, prompt=CONDENSE_QUESTION_PROMPT, verbose=True),
        combine_docs_chain=doc_chain_stream,  # pyright: ignore reportPrivateUsage=none
        verbose=True,
        # rephrase_question=False,
    )
    
    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        try:
            return await fn
        except Exception as e:
            logger.error(f"Caught exception: {e}")
            return None  # Or some sentinel value that indicates failure
        finally:
            event.set()
    
    history = history[-min(len(history), 3):]
    run = asyncio.create_task(
        wrap_done(
            qa_stream.acall({
                "question": message,
                "chat_history": [(pair[0], pair[1]) for pair in history]
            }), 
            callback.done
        )
    )
    
    try:
        async for token in callback.aiter():
            logger.debug("Token: %s", token)
            output += token
            yield output
    except Exception as e:
        logger.error("Error during streaming tokens: %s", e)
            
    await run

# No Stream    
def predict_batch(message, history):
    answering_llm = ChatOpenAI(
        temperature=temperature,
        model=model,
        streaming=False,
        verbose=True,
        callbacks=None,
        openai_api_key=openai_api_key,
    )
    
    doc_chain = load_qa_chain(
        answering_llm, chain_type="stuff", prompt=create_prompt_template(), verbose=True
    )
    
    question_llm = ChatOpenAI(
        temperature=temperature,
        model=model,
        streaming=False,
        verbose=True,
        callbacks=None,
        openai_api_key=openai_api_key,
    )

    qa = ConversationalRetrievalChain(
        retriever=retriever,
        question_generator=LLMChain(
            llm=question_llm, prompt=CONDENSE_QUESTION_PROMPT, verbose=True),
        combine_docs_chain=doc_chain,  # pyright: ignore reportPrivateUsage=none
        verbose=True,
        # rephrase_question=False,
    )
    
    history = history[-min(len(history), 3):]
    
    model_response = qa(
        {
            "question": message,
            "chat_history": [(pair[0], pair[1]) for pair in history]
        }
    )
    print(model_response)
    return model_response['answer']


chatbot_stream = gr.Chatbot(avatar_images=('user.png', 'wishart.png'), bubble_full_width = False)
chatbot_batch = gr.Chatbot(avatar_images=('user.png', 'wishart.png'), bubble_full_width = False)
chat_interface_stream = gr.ChatInterface(predict, 
                 title=title, 
                 description=description, 
                 textbox=gr.Textbox(),
                 chatbot=chatbot_stream,
                 css=css, ) 
chat_interface_batch=gr.ChatInterface(predict_batch, 
                 title=title, 
                 description=description, 
                 textbox=gr.Textbox(),
                 chatbot=chatbot_batch,
                 css=css, ) 

# Gradio Demo 
with gr.Blocks() as demo:

    with gr.Tab("Streaming"):
        # chatbot_stream.like(vote, None, None)
        chat_interface_stream.render()

    with gr.Tab("Batch"):
        # chatbot_batch.like(vote, None, None)
        chat_interface_batch.render()
       
if __name__ == "__main__":
    demo.queue(max_size=10).launch(server_name="0.0.0.0", server_port=7861, debug=True, share=True)