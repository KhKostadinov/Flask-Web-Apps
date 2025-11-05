from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
import ollama
from langchain_core.documents import Document
from langchain_core.runnables import chain, RunnablePassthrough
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_classic.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os, logging

# configure logging
logging.basicConfig(level=logging.INFO)

# CONSTANTS
MODEL_NAME = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text"
ollama.pull(MODEL_NAME)


def loadDoc(file_name: str):
    filePath = './static/files/'+file_name
    if os.path.exists(filePath):
        if file_name.endswith('.pdf'):
            loader = PyPDFLoader(filePath)
        elif file_name.endswith('.docx'):
            loader = Docx2txtLoader(filePath)
        elif file_name.endswith('.txt'):
            loader = TextLoader(filePath, encoding='UTF-8')
        docs = loader.load()
        logging.info("File loaded successfully.")
        return docs
    else:
        logging.error(f"File not found at {filePath}")


def splitDoc(doc): # returned from this function should feed vector_db
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1200, 
                                                   chunk_overlap = 300, 
                                                   add_start_index = True)
    
    all_splits = text_splitter.split_documents(doc)
    return all_splits

def vector_db(all_splits):
    ollama.pull(EMBEDDING_MODEL)
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vStore = Chroma(collection_name="RAG_collection",
                    embedding_function=embeddings,
                    persist_directory="./chroma_rag_db")
    vStore.add_documents(documents=all_splits)
    return vStore

def retriever(vector_db):
    qPrompt = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five
different versions of the given user question to retrieve relevant documents from
a vector database. By generating multiple perspectives on the user question, your
goal is to help the user overcome some of the limitations of the distance-based
similarity search. Provide these alternative questions separated by newlines.
Original question: {question}""",
    )
    retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(),
    llm=ChatOllama(model=MODEL_NAME),
    prompt=qPrompt)
    return retriever

def create_chain(retriever):
    # RAG prompt
    template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    mainChain = ({"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | ChatOllama(model=MODEL_NAME)
    | StrOutputParser()
    )
    return mainChain

def main():
    # load file
    doc = loadDoc("monopoly.pdf")
    # split file
    all_splits = splitDoc(doc)
    # add to vector db
    vDB = vector_db(all_splits)
    # build retriever
    golden_retriever = retriever(vDB)
    # build chain
    myChain = create_chain(golden_retriever)
    question = input("Ask something: ")
    result = myChain.invoke(input = question)
    print(result)

if __name__ == "__main__":
    main()