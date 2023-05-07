FROM debian:bookworm-slim

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN useradd -ms /bin/bash user1
RUN mkdir /home/user1/telegram_bot
WORKDIR /home/user1/telegram_bot
COPY . .
RUN chown -Rh user1:user1 .
USER user1

CMD ["python3", "main.py"]
