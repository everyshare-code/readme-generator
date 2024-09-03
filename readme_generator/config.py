from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        load_dotenv()
        self.extensions = [".py", ".ipynb"]
        self.openai_model = "gpt-4o-mini"
        self.embedding_model = "text-embedding-3-small"

        self.llm = ChatOpenAI(model_name=self.openai_model, temperature=0.3)
        self.code_summary_chain = self.create_code_summary_chain()
        self.readme_chain = self.create_readme_chain()
        self._initialized = True
        self.embeddings = self.create_embeddings()

    def create_readme_chain(self):
        prompt = PromptTemplate.from_template(
            """You are the project leader. Your task is to write a complete README based on the following summary.
                When writing, please write according to the language.
                
            #Language:
            {language}
            
            # Summaries:
            {context}

            # README:
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain

    def create_code_summary_chain(self):
        prompt = PromptTemplate.from_template(
            """You are a code summarization expert. Summarize the following code snippet.
            # Code:
            {context}

            # Summary:
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain

    def create_embeddings(self):
        return OpenAIEmbeddings(model=self.embedding_model, disallowed_special=())
