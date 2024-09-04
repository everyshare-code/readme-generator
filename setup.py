from setuptools import setup, find_packages

setup(
    name="readme_generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain-openai",
        "langchain",
        "tiktoken",
        "scikit-learn",
        "numpy",
        "pandas",
        "transformers",
        "python-dotenv",
        "logging"
    ],
    entry_points={
        "console_scripts": [
            "generate-readme=readme_generator.main:main",
        ],
    },
    author="Park Junyoung",
    author_email="park20542040@gmail.com",
    description="A tool to generate project README files based on code summaries.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/everyshare-code/readme_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
