FROM python:3.10-slim

WORKDIR /app


RUN apt-get update && apt-get install -y build-essential git


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN pip install torch==2.2.2+cpu -f https://download.pytorch.org/whl/torch_stable.html


RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"


COPY app/ .

CMD ["python", "main.py"]

