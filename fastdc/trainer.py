from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import spacy

try:
    spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    print("Downloading 'en_core_web_sm' model...")
    download("en_core_web_sm")

class FastdcTrainer:
    def __init__(self, name="FastdcBot", data_path="data_train.txt"):
        self.chatbot = ChatBot(name)
        self.data_path = data_path

    def train(self):

        """
            Trains the chatbot using a conversation dataset stored in a text file.

            This method reads training data from `self.data_path`, splits it into lines, 
            and feeds it to a `ChatterBot` ListTrainer instance to learn responses.

        """

        trainer = ListTrainer(self.chatbot)
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Training data file '{self.data_path}' not found.")
        with open(self.data_path, "r", encoding="utf-8") as file:
            conversation = file.read().split("\n")
        trainer.train(conversation)

    def get_response(self, message):
        """ 
            Generates a response from the trained chatbot based on the user's input message. 
            Parameters:
            ----------
            message : str
                The input message or question to send to the chatbot.

        """
        return str(self.chatbot.get_response(message))
