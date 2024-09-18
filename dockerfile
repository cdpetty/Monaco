FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD streamlit run --server.port $PORT --server.address 0.0.0.0 --server.enableCORS true --server.enableXsrfProtection false Monaco_Streamlit_App.py