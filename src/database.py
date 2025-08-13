import os
from langchain_huggingface import HuggingFaceEmbeddings
from neo4j import GraphDatabase
from langchain_neo4j import Neo4jVector
import spacy
from dotenv import load_dotenv

class Database:
    load_dotenv()
    def __init__(self, url=None, username=None, password=None):
        self.url = os.getenv('NEO4J_URI')
        self.username = os.getenv('NEO4J_USERNAME')
        self.password = os.getenv('NEO4J_PASSWORD')
        self.driver = self.init_driver(self.url, self.username, self.password)

    def init_driver(self, uri, username, password):
        '''Connects to the Neo4j database and verifies connectivity.'''
        driver = GraphDatabase.driver(uri, auth=(username, password))
        driver.verify_connectivity()
        return driver

    def busca_nome_prof(self, nome_art: str):
        query = '''
        MATCH (p:Professor)-[:PRODUZIU]->(a:Producao{titulo: $nome_art})
        RETURN p.nome AS nome;
        '''
        with self.driver.session() as session:
            try:
                result = session.run(query, nome_art=nome_art)
                return result.data()[0]["nome"]
            except Exception as e:
                print(f"Erro: {e}")
            finally:
                session.close()

    def busca_hindex_prof(self, nome_prof):
        query = '''
        MATCH (p:Professor{nome: $nome_prof})
        RETURN p.hindex as hindex;
        '''
        with self.driver.session() as session:
            try:
                result = session.run(query, nome_prof=nome_prof)
                return result.data()[0]["hindex"]
            except Exception as e:
                print(f"Erro: {e}")
            finally:
                session.close()


class EmbeddingModel:
    def __init__(self, model_name=None, embedding_provider=None):
        load_dotenv()

        self.model_name = os.getenv("MODEL_NAME") or model_name
        self.embedding_provider = embedding_provider or HuggingFaceEmbeddings(
            model_name = self.model_name,
            model_kwargs={"device": "cpu"}
        )

        self.graph = Neo4jVector(
            url=os.getenv('NEO4J_URI'),
            username=os.getenv('NEO4J_USERNAME'),
            password=os.getenv('NEO4J_PASSWORD'),
            embedding=self.embedding_provider,
            index_name="producoes",
            node_label="Producao",
            text_node_property="titulo",
            embedding_node_property="embedding"
        )

        self.nlp = spacy.load("pt_core_news_sm")

    def busca_artigos(self, query: str):
        doc = self.nlp(query.lower())
        filtered_tokens = [
            token.text for token in doc if not token.is_stop and token.is_alpha]
        important_tokens = ' '.join([str(x) for x in filtered_tokens])

        result = self.graph.similarity_search_with_score(query=important_tokens, k=10)

        return [doc for doc in result]