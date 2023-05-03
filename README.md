# Telegram Bot

I'm Cifar10Bot.
You can type messages and I will respond to them.
For example you can ask me current time by typing 'time'.

I can classify images.
You can send me an image with
Plane, Car, Bird, Cat, Deer, Dog, Frog, Horse, Ship or Truck on it.
And I will say, what I see on the image.
I'm not too good at guessing,
because I work with low-quality images.

How to train me:
If you want to make me better at classifying, type 'train X',
where X is a number of epochs you want me to train.

## Установка:
```
git clone git@github.com:VasVol/telegram_bot.git
cd telegram_bot
git checkout dev
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Необходимо проверить, что установлено всё из requirements.txt

## Запуск:
```
python3 main.py
```
