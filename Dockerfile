FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","-c","from reliability import SLO; print('SLO engine ready')"]
