from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings 
from langchain_community.llms import GPT4All
from langchain.chains import RetrievalQA
from langchain.prompts.chat import ChatPromptTemplate


# You need to download a GPT4All model and place it in your desired directory
model_path = "./models/mistral-7b-openorca.Q4_0"

persist_directory = "./storage"
pdf_path = "./docs/description.pdf"

loader = PyMuPDFLoader(pdf_path)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
texts = text_splitter.split_documents(documents)

embeddings = GPT4AllEmbeddings()
vectordb = Chroma.from_documents(documents=texts, 
                                 embedding=embeddings,
                                 persist_directory=persist_directory)
vectordb.persist()

retriever = vectordb.as_retriever(search_kwargs={"k": 3})
#llm = ChatGPT4All(model_path=model_path)
llm = GPT4All(model=model_path, n_threads=8)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Cache dictionary to store previous responses
cache = {}

# Create a ChatPromptTemplate using from_messages
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant for Appollo Hospital that can answer questions based on the PDF document at {pdf_path}."),
    ("human", "{text}")
])

def healthBot(message):
    # Check if the question is already in the cache
    if message in cache:
        return cache[message]
  
    formattedMessage = chat_template.format_messages(pdf_path=pdf_path, text=message)
    query = f"###Prompt {formattedMessage}"
    try:
        llm_response = qa(query)
        response =  (llm_response["result"])
        # Cache the response for future use
        cache[message] = response
        return response
    except Exception as err:
        return('Exception occurred. Please try again', str(err))
