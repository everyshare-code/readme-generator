import os
import fnmatch
import logging
import json
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language


class FileLoader:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_gitignore_patterns(self, root_path: str) -> set[str]:
        gitignore_path: str = os.path.join(root_path, '.gitignore')
        exclude_patterns: set[str] = {
            '__pycache__', 'venv', 'env', '.git', '.idea', '.vscode', 'node_modules'
        }
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if line.endswith('/'):
                            exclude_patterns.add(line.rstrip('/'))
                        else:
                            exclude_patterns.add(line)

        return exclude_patterns

    def is_excluded(self, path: str, exclude_patterns: set[str]) -> bool:
        if os.path.basename(path) == "__init__.py":
            return True

        for pattern in exclude_patterns:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
        return False

    def load_ipynb_file(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)

            code_cells: list[str] = []
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    code_cells.append("".join(cell.get('source', [])))

            return "\n".join(code_cells)

        except Exception as e:
            self.logger.error(f"Error processing Jupyter Notebook file {file_path}: {e}")
            return ""

    def load_file(self, file_path: str) -> str:
        file_extension: str = os.path.splitext(file_path)[1]

        if file_extension == '.ipynb':
            return self.load_ipynb_file(file_path)

        try:
            loader = GenericLoader.from_filesystem(
                file_path,
                suffixes=[file_extension],
                parser=LanguageParser(Language.PYTHON, parser_threshold=30)
            )
            documents = loader.load()
            return "\n".join(doc.page_content for doc in documents)
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {e}")
            return ""

    def load_documents(self, folder_path: str, target_files: list[str], exclude_patterns: set[str]) -> str:
        combined_content: str = ""
        for file in target_files:
            file_path: str = os.path.join(folder_path, file)
            if not self.is_excluded(file_path, exclude_patterns):
                self.logger.info(f"Loading file: {file_path}")
                file_content = self.load_file(file_path)
                combined_content += file_content + "\n"
        return combined_content
