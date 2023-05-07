from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from io import BytesIO
import cv2
import numpy as np
from tensorflow import keras
import datetime

import Globals
import Text

TOKEN = Text.TOKEN
BOT_USERNAME = Text.BOT_USERNAME


class AI:
    def __init__(self):
        self.sum_epochs_count = 0
        (self.x_train, self.y_train),\
            (self.x_test, self.y_test) = keras.datasets.cifar10.load_data()
        self.x_train = self.x_train / Globals.train_k
        self.x_test = self.x_test / Globals.train_k

        self.class_names = Text.class_names

        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Conv2D(Globals.conv_k1, Globals.conv_sizes,
                                           activation='relu',
                                           input_shape=(Globals.conv_k1,
                                                        Globals.conv_k1, 3)))
        self.model.add(keras.layers.MaxPooling2D(Globals.max_pooling_sizes))
        self.model.add(keras.layers.Conv2D(Globals.conv_k2, Globals.conv_sizes,
                                           activation='relu'))
        self.model.add(keras.layers.MaxPooling2D(Globals.max_pooling_sizes))
        self.model.add(keras.layers.Conv2D(Globals.conv_k3, Globals.conv_sizes,
                                           activation='relu'))
        self.model.add(keras.layers.MaxPooling2D(Globals.max_pooling_sizes))
        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(Globals.dense_k1,
                                          activation='relu'))
        self.model.add(keras.layers.Dense(Globals.dense_k2,
                                          activation='softmax'))

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
        await update.message.reply_text(Text.not_trained_text)
        return
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    f = BytesIO(await file.download_as_bytearray())
    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (Globals.image_size, Globals.image_size),
                     interpolation=cv2.INTER_AREA)

    prediction = my_AI.model.predict(np.array([img / Globals.train_k]))
    await update.message.reply_text(
        Text.I_see_text(my_AI.class_names[np.argmax(prediction)])
    )


async def reset_command(update, context):
    global my_AI
    my_AI = AI()
    await update.message.reply_text(Text.reset_command_text)


async def start_command(update, context):
    await update.message.reply_text(Text.start_command_text)


async def help_command(update, context):
    await update.message.reply_text(
        Text.help_command_text,
        parse_mode=ParseMode.HTML
    )


async def generate_response_for_message(text, update, context):
    if text[:len('train ')] == 'train ':
        epochs_count = text[len('train '):]
        try:
            epochs_count = int(epochs_count)
        except ValueError:
            await update.message.reply_text(
                Text.incorrect_train_command_text
            )
        else:
            await update.message.reply_text(
                Text.wait_text(epochs_count * Globals.epoch_time)
            )
            await my_AI.train(epochs_count)
            await update.message.reply_text(Text.can_send_photo_text)
            return

    processed = text.lower()
    a = Text.welcome_user_words

    for elem in a:
        if elem in processed:
            await update.message.reply_text(Text.greeting)
            return

    if "time" in text:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await update.message.reply_text(Text.current_time_text(current_time))
        return

    await update.message.reply_text(Text.dont_understand_text)


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
