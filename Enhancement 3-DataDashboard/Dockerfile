FROM python:3.12-slim

WORKDIR /dashboard

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8050

EXPOSE 8050

CMD ["python", "dashboard.py"]