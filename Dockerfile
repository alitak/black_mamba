FROM python:3.6-slim
COPY ./src/ /app
WORKDIR /app
RUN pip install requests python-dotenv discord
CMD ["python", "black_mamba.py"]