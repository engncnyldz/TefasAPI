FROM python:3.10.14-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

# Upgrade pip, setuptools, and wheel
RUN pip3 install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]