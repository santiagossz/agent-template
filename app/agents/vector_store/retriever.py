import os
from supabase import create_client

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from app.config import vs_cfg, logger


class Retriever:
    doc_type = "pdf"

    def __init__(self, collection: str):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.collection = collection
        self.data_path = os.path.join(
            self.base_path, f"data/{self.collection}.{self.doc_type}"
        )
        self.embeddings = OpenAIEmbeddings()
        self.supabase = create_client(
            vs_cfg.SUPABASE_URL, vs_cfg.SUPABASE_SERVICE_KEY
        ).schema(vs_cfg.SCHEMA)
        self.vector_store = self.connect_supabase_vector_store()

    def load_sql_template(self):
        with open(os.path.join(self.base_path, "sql/pgvector.sql"), "r") as sql_file:
            return sql_file.read()

    def create_collection(self):
        sql_template = self.load_sql_template()
        sql_query = sql_template.format(table_name=self.collection)
        try:
            self.supabase.rpc("pgfunction", {"query": sql_query}).execute()
            return "Collection created successfully"
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return None

    def connect_supabase_vector_store(self):
        return SupabaseVectorStore(
            embedding=self.embeddings,
            client=self.supabase,
            table_name=self.collection,
            query_name=f"match_{self.collection}",
        )

    def load_docs(self):
        loader = PyPDFLoader(self.data_path)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=vs_cfg.CHUNK_SIZE, chunk_overlap=vs_cfg.CHUNK_OVERLAP
        )
        docs = text_splitter.split_documents(pages)

        return docs

    def add_docs_to_vector_store(self):
        try:
            docs = self.load_docs()
            self.vector_store.add_documents(docs)
            return f"Successfully added Docs to VC {self.collection}"
        except Exception as e:
            logger.error(f"Error adding docs to vector store: {e}")
            return None

    def get_relevant_docs(self, value, **kwargs):
        return self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs=kwargs,
        ).invoke(value)
