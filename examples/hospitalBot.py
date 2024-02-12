import os 
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings 
from langchain_community.llms import GPT4All
from langchain.chains import RetrievalQA

# You need to download a GPT4All model and place it in your desired directory
#model_path = "./models/mistral-7b-openorca.Q4_0"
model_path = "orca-mini-3b-gguf2-q4_0.gguf"

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
llm = GPT4All(model = model_path, n_threads=8)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

while True:
        user_input = input("Enter a query: ")
        if user_input == "exit":
            break

        query = f"###Prompt {user_input}"
        try:
            llm_response = qa(query)
            print(llm_response["result"])
        except Exception as err:
            print('Exception occurred. Please try again', str(err))
