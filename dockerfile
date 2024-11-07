FROM python:3.13
RUN pip install -q pypdf
RUN pip install -q python-dotenv
RUN pip install -q langchain
RUN pip install -q langchain-openai
RUN pip install -q openai
RUN pip install -q langchain_community
RUN pip install -q chromadb
RUN pip install -q sentence_transformers


COPY src/main.py main.py
COPY src/tool.py tool.py

CMD python3 main.py