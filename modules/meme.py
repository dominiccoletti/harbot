from .base import Module, ImageUploader
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap
import requests
import os
import io


class Meme(Module, ImageUploader):
    ARGC = 1

    FONT_SIZE = 30
    SMALL_FONT_SIZE = 20
    LARGE_FONT_SIZE = 50
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def list_templates(self):
        return "Supported templates: " + ", ".join(self.templates.keys())

    def __init__(self):
        super().__init__()
        self.templates = {
            "drake": (
                {"position": (350, 100), "center": False},
                {"position": (350, 300), "center": False},
            ),
            "juice": (
                {"position": (327, 145)},
                {"position": (373, 440), "wrap": 25, "font_size": self.SMALL_FONT_SIZE},
            ),
            "changemymind": (
                {"position": (579, 420), "font_size": self.LARGE_FONT_SIZE},
            ),
            "catch": (
                {"position": (250, 90), "color": self.WHITE},
                {"position": (550, 275), "color": self.WHITE},
            ),
            "kirby": (
                {"position": (80, 70), "font_size": self.SMALL_FONT_SIZE, "center": False},
            ),
            "pocket": (
                {"position": (570, 80), "font_size": self.SMALL_FONT_SIZE, "center": False},
            ),
             "brain": (
                {"position": (20, 146), "wrap": 22, "font_size": self.LARGE_FONT_SIZE, "center": False, "center_vertical": True},
                {"position": (20, 450), "wrap": 22, "font_size": self.LARGE_FONT_SIZE, "center": False, "center_vertical": True},
                {"position": (20, 745), "wrap": 22, "font_size": self.LARGE_FONT_SIZE, "center": False, "center_vertical": True},
                {"position": (20, 1040), "wrap": 22, "font_size": self.LARGE_FONT_SIZE, "center": False, "center_vertical": True},
            ),
            "pikachu2": (
                {"position": (10,15),"wrap": 22, "font_size": self.FONT_SIZE, "center": False, "Center_vertical": False},
                {"position": (10,100),"wrap": 22,"font_size": self.FONT_SIZE, "center": False, "Center_vertical": False},
            ),
            "pikachu3": (
                {"position": (10,15),"wrap": 22, "font_size": self.SMALL_FONT_SIZE},
                {"position": (10,67.5),"wrap": 22,"font_size": self.SMALL_FONT_SIZE},
                {"position": (10,135),"wrap": 22,"font_size": self.SMALL_FONT_SIZE},
            ),
            "ask": (
                {"position": (405, 450), "center_vertical": True},
            ),
            "whip": (
                {"position": (406, 438), "color": self.WHITE, "center_vertical": True},
                {"position": (160, 620), "color": self.WHITE, "center_vertical": True},
            ),
            "nut": (
                {"position": (405, 197), "color": self.WHITE, "center_vertical": True},
                {"position": (156, 280), "color": self.WHITE, "center_vertical": True},
            ),
        }
        self.DESCRIPTION = "Generate memes! List the desired template, and then captions each on a new line. " + self.list_templates()

    def response(self, query, message):
        captions = query.split("\n")

        template = captions.pop(0).strip().lower()
        if self.templates.get(template) is None:
            return f"No template found called {template}. " + self.list_templates()
        if len(captions) < len(self.templates[template]):
            return "Not enough captions provided (remember to separate with newlines)."
        image = Image.open(f"resources/memes/{template}.jpg")
        draw = ImageDraw.Draw(image)
        self.mark_image(draw, captions, self.templates[template])
        """
        image.show()
        return
        """
        output = io.BytesIO()
        image.save(output, format="JPEG")
        image_url = self.upload_image(output.getvalue())
        return ("", image_url)

    def mark_image(self, draw: ImageDraw, captions, settings):
        for setting in settings:
            caption = captions.pop(0)
            lines = wrap(caption, setting.get("wrap", 20))
            for line_index, line in enumerate(lines):
                x, y = setting.get("position")
                font = ImageFont.truetype("resources/Lato-Regular.ttf", setting.get("font_size", self.FONT_SIZE))
                if setting.get("center", True):
                    line_width, line_height = draw.textsize(line, font=font)
                    x -= line_width / 2
                draw.text((x, y + line_index * (setting.get("font_size", self.FONT_SIZE) + 5)),
                          line,
                          font=font,
                          fill=setting.get("color", self.BLACK))
