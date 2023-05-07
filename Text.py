TOKEN = "6292004438:AAEYL6PsHiX2rRYmPls5IWptP3_EWRGaO0Q"
BOT_USERNAME = "@Cifar10Bot"

class_names = ['Plane', 'Car', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse',
               'Ship', 'Truck']

reset_command_text = "Learning progress removed."

start_command_text = '''
Hello! I'm Cifar10Bot! Use /help command to see, what I can do.
'''

help_command_text = '''
<b>I'm Cifar10Bot.</b>
You can type messages and I will respond to them.
For example you can ask me current time by typing 'time'.

<b>I can classify images.</b>
You can send me an image with
Plane, Car, Bird, Cat, Deer, Dog, Frog, Horse, Ship or Truck on it.
And I will say, what I see on the image.
I'm not too good at guessing,
because I work with low-quality images.

<b>How to train me:</b>
If you want to make me better at classifying, type 'train X',
where X is a number of epochs you want me to train.
You can use /reset command to remove learning progress.
'''

not_trained_text = "Bot is not trained!"


def I_see_text(item_name):
    return f"In this image I see a {item_name}"


incorrect_train_command_text = '''
Incorrect train command!
Use /help command for more information.
'''


def wait_text(num_of_seconds):
    return ("Please wait a bit, training will take "
            f"about {num_of_seconds} seconds")


can_send_photo_text = "Done! You can now send a photo!"

welcome_user_words = ["hello", "hi", "hey"]

greeting = "Hey there!"

dont_understand_text = "I don't understand. Use /help command to see what " \
                       "I can do."


def current_time_text(str_time):
    return "Current time is " + str_time
