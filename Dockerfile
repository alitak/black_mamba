FROM python:3.6-slim
RUN pip install requests discord
COPY ./src/ /app
WORKDIR /app
CMD ["python", "black_mamba.py"]