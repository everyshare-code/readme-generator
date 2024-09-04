from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.runnables.base import RunnableSequence


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
        self.extensions: list[str] = [".py", ".ipynb"]
        self.openai_model: str = "gpt-4o-mini"
        self.embedding_model: str = "text-embedding-3-small"

        self.llm: ChatOpenAI = ChatOpenAI(model_name=self.openai_model, temperature=0.3)
        self.code_summary_chain: RunnableSequence = self.create_code_summary_chain()
        self.readme_chain: RunnableSequence = self.create_readme_chain()
        self.final_readme_chain: RunnableSequence = self.create_final_readme_chain()
        self._initialized: bool = True
        self.embeddings = self.create_embeddings()

    def create_readme_chain(self) -> RunnableSequence:
        prompt: PromptTemplate = PromptTemplate.from_template(
            """You are the project leader. Your task is to write a complete README based on the following summary.
                When writing, please write according to the language.

            # Language:
            {language}

            # Summaries:
            {context}

            # README:
            """
        )
        chain: RunnableSequence = prompt | self.llm | StrOutputParser()
        return chain

    def create_code_summary_chain(self) -> RunnableSequence:
        prompt: PromptTemplate = PromptTemplate.from_template(
            """You are a code summarization expert. Summarize the following code snippet.
            # Code:
            {context}

            # Summary:
            """
        )
        chain: RunnableSequence = prompt | self.llm | StrOutputParser()
        return chain

    def create_final_readme_chain(self):
        prompt: PromptTemplate = PromptTemplate.from_template(
            """
            You are the project leader. Your task is to write a comprehensive and professional README for the entire project.
            The README should include the following sections:
            
            # 프로젝트 명:
            Provide a concise title for the project.
            
            # 프로젝트 설명:
            Provide an overview of the project, including its purpose, features, and goals.
            
            # 프로젝트 설명 및 의존성:
            Explain how to install the project. Include dependencies and any necessary setup steps.
            
            # 사용법:
            Provide instructions for using the project, including key commands or workflows.
            
            # 예시:
            Provide an example of how the project can be used, if applicable.
            
            # 프로젝트 파일 구조:
            Provide a summary of the project’s folder and file structure.
            
            # 기여:
            Explain how others can contribute to the project.
            
            # 라이센스:
            State the project's license type and any related details.
            
            # 프로젝트 문의:
            Include how users or contributors can get in touch with the project team or maintainers.
            
            # Summaries:
            {context}
            
            # README:         
            """
        )
        chain: RunnableSequence = prompt | self.llm | StrOutputParser()
        return chain
    def create_embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(model=self.embedding_model, disallowed_special=())
