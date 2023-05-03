# Telegram Bot

"<b>I'm Cifar10Bot.</b>\n"
"You can type messages and I will respond to them.\n"
"For example you can ask me current time by typing 'time'.\n\n"

"<b>I can classify images.</b>\n"
"You can send me an image with\n"
"Plane, Car, Bird, Cat, Deer, Dog, Frog, Horse, Ship or Truck on it.\n"
"And I will say, what I see on the image.\n"
"I'm not too good at guessing,\n"
"because I work with low-quality images.\n\n"

"<b>How to train me:</b>\n"
"If you want to make me better at classifying, type 'train X',\n"
"where X is a number of epochs you want me to train.\n"
"You can use /reset command to remove learning progress.\n",

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
