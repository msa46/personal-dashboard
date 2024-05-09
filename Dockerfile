FROM python:3.12-alpine
WORKDIR /code
ENV REACT_VERSION=18.2.0
COPY . .
RUN pip install -r requirements.text
EXPOSE 8050

CMD ["python","index.py"]
