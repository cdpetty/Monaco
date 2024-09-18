FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD streamlit run --server.port 8080 --server.enableCORS false monaco/streamlit_app_side_by_side.py