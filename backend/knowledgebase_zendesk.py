from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
import os
import openai
import pinecone
from tqdm import tqdm

from constants import dataset_folder, ALLOWED_FILES
from parsers.doc import process_doc
from parsers.docx import process_docx
from parsers.pdf import process_pdf
from parsers.powerpoint import process_powerpoint
from parsers.xlsx import process_xlsx

file_processors = {
    ".pdf": process_pdf,
    ".pptx": process_powerpoint,
    ".doc": process_doc,
    ".docx": process_docx,
    ".xlsx": process_xlsx,
    ".xls": process_xlsx,
}

# OpenAI function to generate embeddings
# def get_embeddings(text):
#     response = openai.Embedding.create(input=text, model="text-similarity-davinci-001")
#     return response["data"][0]["embedding"]

def construct_knowledgebase_zendesk(file_path):
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENV"),
    )
    index_name = os.getenv("PINECONE_INDEX_NAME")
    index = pinecone.Index(index_name)
    
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = Pinecone(index, embeddings, "text")
    
    with open(file_path, 'r') as f:
        text = f.read()
    
    documents = text.split('================================================================================\n')
    documents = [d.split('\n\n')[1] for d in documents if len(d) > 10]
    
    # for d in tqdm(documents):
    #     vectorstore.add_texts([d], index_name=index_name)
    vectorstore.add_texts(documents, index_name=index_name)
    
    
    print(len(documents))
    # if index_name not in pinecone.list_indexes():
    #     pinecone.create_index(index_name, dimension=1536, metric="cosine")
    
    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # for root, dirs, files in os.walk(dataset_folder):
    #     for file in tqdm(files, desc=f"Processing files in {root}"):
    #         if file.endswith(tuple(ALLOWED_FILES)):
    #             file_extension = os.path.splitext(file)[1]
    #             documents = file_processors[file_extension](os.path.join(root, file))
    #             docs = text_splitter.split_documents(documents)
    #             vectorstore.add_documents(documents=docs, index_name=index_name)


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    construct_knowledgebase_zendesk('Zendesk_history.txt')