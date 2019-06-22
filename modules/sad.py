from .base import Module
import random


class Sad(Module):
    DESCRIPTION = "Instantly dispel all mental health problems"
    PICTURES = [
        "https://i.groupme.com/1600x760.jpeg.20c03d30afa64f52a65c6f896f5c32dd.large",
        "https://i.groupme.com/600x415.jpeg.9b3642af63514f74b190b08d14c4cffc.large",
        "https://i.groupme.com/500x503.jpeg.99cef87c76e84fbbb74be58d68496720.large",
        "https://i.groupme.com/1280x678.jpeg.91b555f2b2f34390819cfed90793d768.large",  # cat
    ]

    def response(self, query, message):
        return random.choice(self.PICTURES)
