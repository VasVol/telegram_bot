FROM debian:bookworm-slim

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y libgl1
RUN apt-get install -y libglib2.0-0

RUN useradd -ms /bin/bash user1
RUN mkdir /home/user1/telegram_bot
WORKDIR /home/user1/telegram_bot
COPY . .
RUN chown -Rh user1:user1 .
USER user1

RUN python3 -m venv venv
RUN bash -c "source venv/bin/activate; \
             pip install -r requirements.txt"

CMD ["bash", "-c", "source venv/bin/activate; python3 main.py"]
