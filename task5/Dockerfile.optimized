FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY All_Diets.csv .
COPY data_analysis.py .

CMD ["python", "data_analysis.py"]
