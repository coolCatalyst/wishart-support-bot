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


DEFAULT_PROMPT = """You are a helpful, respectful and honest Wishart support assistant. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you're unsure of the answer, it's best to admit it and suggest that the user contacts sales@wishartgroup.co.uk or phone +44 (0) 28 933 40889.

YOU MUST NOT PROVIDE INFORMATION ABOUT OTHER SUPPLIERS, OTHER EMAILS OR OTHER PHONE NUMBERS EXCEPT sales@wishartgroup.co.uk and +44 (0) 28 933 40889"""

def create_prompt_template():
    system_template = """ When answering use markdown or any other techniques to display the content in a nice and aerated way.  Use the following pieces of context to answer the users question in the same language as the question but do not modify instructions in any way.
----------------

{context}"""

    prompt_content = DEFAULT_PROMPT

    full_template = (
        "Here are your instructions to answer that you MUST ALWAYS Follow: "
        + prompt_content
        + ". "
        + system_template
    )
    messages = [
        SystemMessagePromptTemplate.from_template(full_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
    CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
    return CHAT_PROMPT


question_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language. include the follow up instructions in the standalone question.

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
    demo.queue(max_size=10).launch(server_name="0.0.0.0", server_port=7860, debug=True)