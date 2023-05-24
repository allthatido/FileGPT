"""
DB class to load ans store data into vector stores
"""
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


class Data:
    """
    Class for data handling
    """

    def __init__(self, file):
        self.vector_db = None
        self.retriever = None
        self.documents = None
        self.db_dir = 'db'
        self.data_dir = 'data'
        self.file = file

    def load_docs(self):
        """
        load file to extract pages
        """
        self.documents = PyPDFLoader(os.path.join(
            self.data_dir, self.file.name)).load_and_split()

    def gen_vectorstore(self, chunk_size=450, chunk_overlap=50):
        """
        create/load saved embedding in/from a persitant vector store db
        """

        embeddings = HuggingFaceEmbeddings()

        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        if len(os.listdir(self.db_dir)) == 0:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunks = text_splitter.split_documents(self.documents)
            self.vector_db = Chroma.from_documents(
                documents=chunks, embedding=embeddings, persist_directory=self.db_dir)
            self.vector_db.persist()
            self.retriever = self.vector_db.as_retriever(
                search_kwargs={"k": 1})
        elif len(os.listdir(self.db_dir)) != 0:
            self.vector_db = Chroma(persist_directory=self.db_dir,
                                    embedding_function=embeddings)
            self.retriever = self.vector_db.as_retriever(
                search_kwargs={"k": 1})
