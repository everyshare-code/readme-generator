import os
import logging
from readme_generator.file_loader import FileLoader
from readme_generator.readme_creator import ReadmeCreator

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReadmeGenerator:
    def __init__(self, root_path: str, extensions: list[str]):
        self.root_path: str = root_path
        self.extensions: list[str] = extensions
        self.file_loader: FileLoader = FileLoader()
        self.readme_creator: ReadmeCreator = ReadmeCreator()

    def generate_project_readme(self) -> None:
        try:
            exclude_patterns = self.file_loader.load_gitignore_patterns(self.root_path)

            # 폴더별로 README 생성 및 요약 수집
            folder_readmes = self.generate_folder_readmes(exclude_patterns)

            # 전체 프로젝트 README 생성
            if folder_readmes:
                logger.info("Generating final project README.")
                final_readme_content = self.readme_creator.create_final_readme(folder_readmes)
                if final_readme_content:
                    readme_path: str = os.path.join(self.root_path, "README.md")
                    with open(readme_path, "w") as f:
                        f.write(final_readme_content)
                    logger.info(f"Final README generated at: {readme_path}")
                else:
                    logger.warning("Final README content is empty.")
            else:
                logger.warning("No folder readmes were generated.")
        except Exception as e:
            logger.error(f"An error occurred during README generation: {e}")

    def generate_folder_readmes(self, exclude_patterns: set[str]) -> list[str]:
        folder_readmes: list[str] = []

        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if not self.file_loader.is_excluded(os.path.join(root, d), exclude_patterns)]

            target_files = [f for f in files if any(f.endswith(ext) for ext in self.extensions)]
            if target_files:
                combined_content = self.file_loader.load_documents(root, target_files, exclude_patterns)
                readme_content = self.readme_creator.create_readme_for_folder(combined_content)
                if readme_content:
                    folder_summary: str = f"## {os.path.basename(root)}\n{readme_content}\n"
                    folder_readmes.append(folder_summary)
                    logger.info(f"README generated for folder: {root}")

        return folder_readmes

# 메인 함수
if __name__ == "__main__":
    project_path: str = '/Users/everyshare/readme_generator'
    extensions: list[str] = [".py", ".ipynb"]
    generator = ReadmeGenerator(project_path, extensions)
    generator.generate_project_readme()
