from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from io import BytesIO
import cv2
import numpy as np
from tensorflow import keras
import datetime

TOKEN = "6292004438:AAEYL6PsHiX2rRYmPls5IWptP3_EWRGaO0Q"
BOT_USERNAME = "@Cifar10Bot"


class AI:
    def __init__(self):
        self.sum_epochs_count = 0
        (self.x_train, self.y_train),\
            (self.x_test, self.y_test) = keras.datasets.cifar10.load_data()
        self.x_train = self.x_train / 255
        self.x_test = self.x_test / 255

        self.class_names = ['Plane', 'Car', 'Bird', 'Cat', 'Deer', 'Dog',
                            'Frog', 'Horse', 'Ship', 'Truck']

        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Conv2D(32, (3, 3), activation='relu',
                                           input_shape=(32, 32, 3)))
        self.model.add(keras.layers.MaxPooling2D(2, 2))
        self.model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
        self.model.add(keras.layers.MaxPooling2D(2, 2))
        self.model.add(keras.layers.Conv2D(128, (3, 3), activation='relu'))
        self.model.add(keras.layers.MaxPooling2D(2, 2))
        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(128, activation='relu'))
        self.model.add(keras.layers.Dense(10, activation='softmax'))

        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])

    async def train(self, epochs_count):
        self.model.fit(self.x_train, self.y_train, epochs=epochs_count,
                       validation_data=(self.x_test, self.y_test))
        self.sum_epochs_count += epochs_count


my_AI = AI()


async def handle_photo(update, context):
    if my_AI.sum_epochs_count == 0:
        await update.message.reply_text(
            "Bot is not trained!"
        )
        return
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    f = BytesIO(await file.download_as_bytearray())
    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)

    prediction = my_AI.model.predict(np.array([img / 255]))
    await update.message.reply_text(
        f"In this image I see a {my_AI.class_names[np.argmax(prediction)]}"
    )


async def reset_command(update, context):
    global my_AI
    my_AI = AI()
    await update.message.reply_text(
        "Learning progress removed."
    )


async def start_command(update, context):
    await update.message.reply_text(
        "Hello! I'm Cifar10Bot! Use /help command to see, what I can do."
    )


async def help_command(update, context):
    await update.message.reply_text(
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
        "where X is a number of epochs you want me to train.",
        parse_mode=ParseMode.HTML
    )


async def generate_response_for_message(text, update, context):
    if text[:6] == 'train ':
        epochs_count = text[6:]
        try:
            epochs_count = int(epochs_count)
        except ValueError:
            await update.message.reply_text(
                "Incorrect train command!\n"
                "Use /help command for more information."
            )
        else:
            await update.message.reply_text(
                "Please wait a bit, training will take "
                f"about {epochs_count * 10} seconds"
            )
            await my_AI.train(epochs_count)
            await update.message.reply_text("Done! You can now send a photo!")
            return

    processed = text.lower()
    a = ["hello", "hi", "hey"]

    for elem in a:
        if elem in processed:
            await update.message.reply_text("Hey there!")
            return

    if "time" in text:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await update.message.reply_text("Current time is " + current_time)
        return

    await update.message.reply_text(
        "I don't understand. Use /help command to see what I can do."
    )


async def handle_message(update, context):
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == "group" and BOT_USERNAME in text:
        text = text.replace(BOT_USERNAME, "").strip()
    await generate_response_for_message(text, update, context)


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling(poll_interval=1)
