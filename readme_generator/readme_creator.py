import logging
import tiktoken
import numpy as np
from sklearn.cluster import KMeans
from langchain_text_splitters import RecursiveCharacterTextSplitter
from readme_generator.config import Config


def count_tokens(text, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    return len(tokens)


class ReadmeCreator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ReadmeCreator, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.config = Config()
        self.code_summary_chain = self.config.code_summary_chain
        self.readme_chain = self.config.readme_chain
        self.splitter = RecursiveCharacterTextSplitter.from_language(
            language="python", chunk_size=2048, chunk_overlap=100  # chunk size를 적절히 조정
        )
        self.embeddings_model = self.config.embeddings  # 텍스트 임베딩을 위해 OpenAI 임베딩 사용
        self._initialized = True

    def cluster_and_select_representatives(self, documents, max_clusters=5):
        logging.info(f"Clustering {len(documents)} documents into up to {max_clusters} clusters.")

        # 문서 임베딩 생성
        embeddings = [self.embeddings_model.embed_query(text=doc) for doc in documents]
        embeddings_matrix = np.array(embeddings)

        # 클러스터 수를 문서 수에 맞게 조정
        num_clusters = min(max_clusters, len(documents))

        if num_clusters <= 1:
            logging.warning("Not enough documents to form clusters. Returning original documents.")
            return documents

        # KMeans 클러스터링
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(embeddings_matrix)
        labels = kmeans.labels_

        # 각 클러스터에서 대표 문서 선택
        representative_docs = []
        for cluster_id in range(num_clusters):
            cluster_docs = [doc for doc, label in zip(documents, labels) if label == cluster_id]
            if cluster_docs:
                representative_docs.append(cluster_docs[0])  # 첫 번째 문서를 대표로 선택 (다른 전략으로 변경 가능)

        logging.info(f"Selected {len(representative_docs)} representative documents from clusters.")
        return representative_docs

    def create_readme_for_folder(self, combined_content, language="kor"):
        logging.info(f"Creating README for folder with content size: {len(combined_content)}")

        split_documents = self.splitter.split_text(combined_content)

        # 청크 크기를 토큰 수로 제한
        valid_documents = []
        for doc in split_documents:
            token_count = count_tokens(doc, model=self.config.openai_model)
            if token_count <= 4096:  # API의 제한을 넘지 않도록 설정
                valid_documents.append(doc)

        if not valid_documents:
            logging.error("No valid documents to summarize.")
            return None

        # 클러스터링 후 대표 문서 선택
        representative_docs = self.cluster_and_select_representatives(valid_documents)

        # 대표 문서 요약
        summarized_chunks = self.code_summary_chain.batch([{"context": doc} for doc in representative_docs])

        # 요약된 내용을 병합하여 최종 README 생성
        summarized_text = "\n".join(summarized_chunks)
        readme_content = self.readme_chain.invoke({"language": language, "context": summarized_text})

        if not readme_content:
            logging.error("The model returned None for the README content.")
        return readme_content

    def create_final_readme(self, combined_summaries, language="kor"):
        """전체 프로젝트에 대한 최종 README를 생성합니다."""
        readme_content = self.readme_chain.invoke({"language": language,"context": combined_summaries})

        if not readme_content:
            logging.error("The model returned None for the README content.")
        return readme_content
