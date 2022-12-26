FROM python:3.9

WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002
ENV PORT=5002

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"] 