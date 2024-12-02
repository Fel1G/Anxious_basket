FROM python:alpine
ENV PYTHONPATH=/app/src
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements/base.txt
RUN pip install --no-cache-dir -r requirements/prod.txt
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]