# pip install python-telegram-bot
# pip install tensorflow
# pip install numpy
# pip install opencv-python
from telegram.ext import Application, CommandHandler, MessageHandler, filters, \
    ContextTypes

from io import BytesIO
import cv2
import numpy as np
from tensorflow import keras
import datetime
import os

print("Starting up bot...")

TOKEN = "6078048516:AAFJElCZkGyqXzp0EAUicd9PATxa0WzeuFg"
BOT_USERNAME = "@VolovichBot"


class AI:
    def __init__(self):
        (self.x_train, self.y_train), (self.x_test, self.y_test) = keras.datasets.cifar10.load_data()
        self.x_train = self.x_train / 255
        self.x_test = self.x_test / 255

        self.class_names = ['Plane', 'Car', 'Bird', 'Cat', 'Deer', 'Dog',
                            'Frog', 'Horse', 'Ship', 'Truck']

        k = 3
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Conv2D(32, (k, k), activation='relu',
                                           input_shape=(32, 32, 3)))
        self.model.add(keras.layers.MaxPooling2D(2, 2))
        self.model.add(keras.layers.Conv2D(64, (k, k), activation='relu'))
        self.model.add(keras.layers.MaxPooling2D(2, 2))
        self.model.add(keras.layers.Conv2D(64, (k, k), activation='relu'))
        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(64, activation='relu'))
        self.model.add(keras.layers.Dense(10, activation='softmax'))

    async def train(self, update, context):
        # if os.path.exists('cifar_classifier.model'):
        #     self.model = keras.models.load_model('cifar_classifier.model')
        # else:
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])
        self.model.fit(self.x_train, self.y_train, epochs=10,
                       validation_data=(self.x_test, self.y_test))
        self.model.save('cifar_classifier.model')


my_AI = AI()


# Handles a photo
async def handle_photo(update, context):
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    f = BytesIO(await file.download_as_bytearray())
    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)

    prediction = my_AI.model.predict(np.array([img / 255]))
    await update.message.reply_text(
        f"In this image I see a {my_AI.class_names[np.argmax(prediction)]}")


# Lets us use the /start command
async def start_command(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello, I'm an AI that can look at photo and say, what I see on them: Plane, Car, Bird, Cat, Deer, Dog, Frog, Horse, Ship or Truck.\n"
        "Use /train command to train me.")


async def help_command(update, context: ContextTypes.DEFAULT_TYPE):
    await start_command(update, context)


async def train_command(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please wait a bit, training takes about 1 minute")
    await my_AI.train(update, context)
    await update.message.reply_text("Done! You can now send a photo!")


def handle_response(text: str) -> str:
    # Create your own response logic
    processed: str = text.lower()
    a = ["hello", "hi", "hey"]

    for elem in a:
        if elem in processed:
            return "Hey there!"

    if "time" in text:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return "Current time is " + current_time

    return "I don't understand. Use /help to see what I can do."


async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f"User ({update.message.chat.id}) in {message_type}: {text}")

    # React to group messages only if users mention the bot directly
    if message_type == "group":
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it"s not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print("Bot:", response)
    await update.message.reply_text(response)


# # Log errors
# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(f"Update {update} caused error {context.error}")

# Run the program
if __name__ == "__main__":
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", start_command))
    app.add_handler(CommandHandler("train", train_command))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Log all errors
    # app.add_error_handler(error)

    print("Polling...")
    # Run the bot
    app.run_polling(poll_interval=1)
