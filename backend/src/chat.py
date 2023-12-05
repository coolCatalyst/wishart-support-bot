import asyncio
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
import logging
from typing import Awaitable

from src.prompt import CHAT_PROMPT, CONDENSE_QUESTION_PROMPT

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

async def inference_stream(message, history, model, temperature, openai_api_key, retriever):
    history = history[-min(len(history), 3):]
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
        answering_llm_stream, chain_type="stuff", prompt=CHAT_PROMPT, verbose=True
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
def inference(message, history, model, temperature, openai_api_key, retriever):
    answering_llm = ChatOpenAI(
        temperature=temperature,
        model=model,
        streaming=False,
        verbose=True,
        callbacks=None,
        openai_api_key=openai_api_key,
    )
    
    doc_chain = load_qa_chain(
        answering_llm, chain_type="stuff", prompt=CHAT_PROMPT, verbose=True
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

