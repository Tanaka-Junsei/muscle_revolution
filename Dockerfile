FROM python:3.11
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot

EXPOSE 8080

CMD ["python", "bot.py"]
