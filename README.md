# Python 프로젝트 README 생성기

---

## 소개
`readme_generator`는 Python 패키지로, 프로젝트의 README 파일을 자동으로 생성하는 도구입니다. 이 패키지는 사용자가 손쉽게 프로젝트에 대한 정보를 정리하고 공유할 수 있도록 도와줍니다.

---

## 패키지 정보

- **버전**: 0.1.0
- **필수 의존성**:
  - langchain-openai
  - langchain-community
  - tiktoken
  - scikit-learn
  - numpy
  - pandas
  - transformers
  - python-dotenv
  - logging

---

## ReadmeCreator 클래스

이 프로젝트는 `ReadmeCreator`라는 싱글톤 클래스를 정의하여 README 파일을 생성하고 관리하는 기능을 제공합니다. 이 클래스는 `__new__` 메서드를 사용하여 단 하나의 인스턴스만 생성되도록 보장합니다. 초기화 과정에서 다양한 구성 설정, 파이썬 코드 처리를 위한 텍스트 분할기, 텍스트 표현을 위한 임베딩 모델을 설정합니다.

### 주요 기능

#### ReadmeCreator 클래스

- **클러스터링 및 대표 문서 선택**: 
  - `cluster_and_select_representatives` 메서드는 문서 목록을 받아 KMeans 클러스터링을 통해 임베딩 기반으로 클러스터링을 수행합니다. 클러스터링할 문서 수를 로깅하고 각 클러스터에서 대표 문서를 선택하여 반환합니다. 클러스터를 형성할 만큼의 문서가 부족할 경우 원본 문서를 반환합니다.

- **README 생성 메서드**:
  1. **`create_readme_for_folder(self, combined_content, language="kor")`**:
     - 입력 콘텐츠의 크기를 로깅합니다.
     - 텍스트 분할기를 사용하여 콘텐츠를 더 작은 문서로 분할합니다.
     - API 제약을 준수하기 위해 토큰 수가 4096을 초과하는 문서를 필터링합니다.
     - 유효한 문서가 남지 않을 경우 오류를 로깅하고 `None`을 반환합니다.
     - 유효한 문서를 클러스터링하고 대표 문서를 선택합니다.
     - 선택된 대표 문서를 요약하여 청크로 나눕니다.
     - 요약된 청크를 병합하여 최종 README 콘텐츠를 생성합니다.
     - README 콘텐츠 생성에 실패할 경우 오류를 로깅합니다.

  2. **`create_final_readme(self, combined_summaries, language="kor")`**:
     - 전체 프로젝트에 대한 최종 README를 생성합니다.
     - 첫 번째 메서드와 유사하게 체인을 호출하여 README를 생성하며, 콘텐츠 생성에 실패할 경우 오류를 로깅합니다.

### Config 클래스

- **싱글톤 패턴**: 클래스의 단일 인스턴스만 생성되도록 보장합니다.
- **초기화**: 환경 변수를 로드하고 다양한 속성을 한 번만 초기화합니다.
- **모델 구성**: OpenAI의 언어 처리 및 임베딩을 위한 모델을 설정합니다.
- **체인 생성**: README 파일 생성 및 코드 스니펫 요약을 위한 처리 체인을 생성하는 메서드를 정의합니다.

### FileLoader 클래스

- **파일 로딩 관리**: `.gitignore` 파일 및 Jupyter Notebook(`.ipynb`) 파일을 처리하는 데 중점을 둡니다.
  
- **`.gitignore` 패턴 로딩**: `load_gitignore_patterns` 메서드는 주어진 경로에서 `.gitignore` 파일을 읽고 제외할 패턴을 추출합니다.
  
- **제외 체크**: `is_excluded` 메서드는 주어진 파일 경로가 제외 패턴에 따라 제외되어야 하는지 확인합니다.
  
- **Jupyter Notebook 로딩**: `load_ipynb_file` 메서드는 Jupyter Notebook 파일을 읽고 모든 코드 셀을 추출하여 결합된 소스 코드를 문자열로 반환합니다.
  
- **파일 로딩**: `load_file` 메서드는 파일의 확장자에 따라 파일 유형을 결정하고 적절한 로딩 메서드를 호출합니다.

### Token Counting

- **`count_tokens` 함수**: 주어진 문자열 `text`와 선택적 매개변수 `model`(기본값: "gpt-4")을 받아 `tiktoken` 라이브러리를 사용하여 텍스트를 토큰으로 인코딩하고 총 토큰 수를 반환합니다.

---

## 사용법

1. 필요한 라이브러리를 설치합니다. (requirements.txt 파일 참고)
2. 환경 변수를 설정합니다. (.env 파일에 openai API key를 입력하거나 환경변수에 등록합니다.)
3. `ReadmeCreator` 클래스를 인스턴스화하고 필요한 메서드를 호출하여 README 파일을 생성합니다.


```python
project_path = '/Users/everyshare/readme_generator'
extensions = [".py", ".ipynb"]
generator = ReadmeGenerator(project_path, extensions)
generator.generate_project_readme()
```

이 명령어를 실행하면 `project_path` 경로의 프로젝트 정보를 바탕으로 README 파일이 생성됩니다.

---

## 기여

이 프로젝트에 기여하고 싶으신 분들은 이슈를 열거나 풀 리퀘스트를 제출해 주세요.

---

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

---

