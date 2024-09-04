# 프로젝트 명:
readme_generator

# 프로젝트 설명:
`readme_generator`는 README 파일을 자동으로 생성하는 Python 패키지입니다. 이 도구는 프로젝트의 문서화를 간소화하고, 일관된 형식으로 README 파일을 작성하는 데 도움을 줍니다. 사용자는 이 패키지를 통해 프로젝트의 구조와 내용을 기반으로 쉽게 README 파일을 만들 수 있으며, 이를 통해 프로젝트의 가독성과 유지보수성을 향상시킬 수 있습니다.

## 주요 기능:
- 자동으로 README 파일 생성
- 다양한 파일 형식 지원
- 클러스터링 및 대표 문서 선택 기능
- 설정 관리 및 환경 변수 로드

## 목표:
- 프로젝트 문서화의 효율성을 높이고, 개발자들이 일관된 형식으로 문서를 작성할 수 있도록 지원합니다.

# 프로젝트 설명 및 의존성:
이 패키지를 설치하려면 다음 명령어를 사용하세요:

```bash
pip install readme_generator
```

## 의존성:
이 패키지는 다음과 같은 라이브러리에 의존합니다:
- langchain
- langchain-openai
- scikit-learn

# 예시:
1. 프로젝트를 클론합니다.
2. 필요한 패키지를 설치합니다.
3. `ReadmeGenerator` 클래스를 사용하여 원하는 디렉토리의 README 파일을 생성합니다.

```python
from readme_generator import ReadmeGenerator

generator = ReadmeGenerator(root_path='your_project_directory', extensions=['.py', '.md'])
generator.generate_project_readme()
```

# 프로젝트 파일 구조:
```
readme_generator/
├── README.md
├── LICENSE
├── setup.py
└── readme_generator/
   ├── __init__.py
   ├── readme_creator.py
   ├── readme_generator.py
   ├── config.py
   └── file_loader.py
```

# 기여:
기여를 원하신다면, 이 프로젝트의 GitHub 저장소를 방문해 주세요. 이슈를 제기하거나 풀 리퀘스트를 제출하여 프로젝트에 기여할 수 있습니다.

# 라이센스:
이 패키지는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

# 프로젝트 문의:
이 패키지는 **Park Junyoung**에 의해 개발되었습니다. 문의 사항이 있으시면 아래의 연락처로 연락해 주세요.
- 이메일: park20542040@gmail.com