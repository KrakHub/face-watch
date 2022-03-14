FROM python:3.9.10-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt update && apt install -y cmake
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "python3", "-m", "run", "--host=0.0.0.0", "python zombdetector.py"]