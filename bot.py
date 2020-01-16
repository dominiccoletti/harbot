import modules
import os
import re
import requests
import json
import difflib
from flask import Flask, request, render_template


app = Flask(__name__)
with open("groups.json", "r") as f:
    GROUPS = json.load(f)

MAX_MESSAGE_LENGTH = 1000
PREFIX = "!"

static_commands = {
    "ping": "Pong!",
	"sharp": ("", "https://i.groupme.com/960x960.jpeg.83b694dec83a40629c3ef63053cedf83.large"),
    "sam": "❗❗❗N O 💪 F L E X 💪 Z O N E ❗❗❗",
    "quack": "quack",
    "test": "http://ricepuritytest.com",
    "dislike": "👎😬👎\n 🦵🦵",
    "shrug": r"¯\_(ツ)_/¯",
    "snort": "😤",
    "oh": ("", "https://i.groupme.com/766x750.jpeg.9209520c57e848369444ca498e31f90a.large"),
    "victors": "Hail! To the Victors Valiant\nHail! To the Conquering Heroes\nHail! Hail! To Michigan\nThe Leaders and Best\n\nHail! To the Victors Valiant\nHail! To the Conquering Heroes\nHail! Hail! To Michigan\nThe Champions of the West",
    "popcorn": "https://www.youtube.com/watch?v=9nwOm4AAXwc",
    "bang": ("", "https://i.groupme.com/720x1440.png.c76127a21867451093edd11bbb09d75d.large"),
    "oof": ("Oh?", "https://i.groupme.com/1500x1125.jpeg.9b2c341aa9854831ab2525d7e21e974a.large"),
    "amma": ("", "https://i.groupme.com/714x456.jpeg.66fb9e9dacab4cd9b860b084eceff282.large"),
    "tease": ("", "https://i.groupme.com/936x1246.jpeg.d0d60970b329415cac1d7a1825a783a7.large"),
    "chike": ("", "https://i.groupme.com/1021x1400.jpeg.70192657c76745ab809357d0512d4951.large"),
    "ohno": ("", "https://i.groupme.com/1280x720.jpeg.f7c11a529a3b4a7195f71fa6be5ebfef.large"),
    "pressed": ("", "https://i.groupme.com/540x719.jpeg.2229bdb9f15247a7a112ac0be95e065a.large"),
    "docschedule": ("https://undergrad.admissions.columbia.edu/welcome/visit/columbia-college-days-campus", ""),
    "flex": "👮🏽🚨🚔 PULL OVER 👮🏽🚨🚔\n\n😤Put your hands behind your back😤\n\n🗣I'm taking you into custody🗣\n\n📝And registering you as a📝\n\n🔥😩FLEX OFFENDER😩🔥",
}

commands = {
    "zalgo": modules.Zalgo(),
    "flip": modules.Flip(),
    "groups": modules.Groups(),
    "about": modules.About(),
    "xkcd": modules.XKCD(),
    "elizabeth": modules.Elizabeth(),
    "dania": modules.Dania(),
    "jake": modules.Jake(),
    "carlos": modules.Carlos(),
    "crista": modules.Crista(),
    "maria": modules.Maria(),
    "annie": modules.Annie(),
    "renee": modules.Renee(),
    "victor": modules.Victor(),
    "weather": modules.Weather(),
    "fightosu": modules.Fightosu(),
    "sad": modules.Sad(),
    "nato": modules.NATO(),
    "eightball": modules.EightBall(),
    "analytics": modules.Analytics(),
    "youtube": modules.YouTube(),
    "pick": modules.Pick(),
    "chose": modules.Chose(),
    "meme": modules.Meme(),
    "love": modules.Love(),
    "price": modules.Price(),
    "minion": modules.Minion(),
    "house": modules.House(),
    "location": modules.Location(),
    "twitter": modules.Twitter(),
    "tea": modules.Tea(),
    "lyrics": modules.Lyrics(),
    "nasa": modules.NASA(),
    "amber": modules.Amber(),
    "uwu": modules.UWU(),
    "conversationstarter": modules.ConversationStarter(),
    "quote": modules.Quote(),
    "dog": modules.Dog(),
    "funfact": modules.FunFact(),
    "kelbo": modules.Kelbo(),
    "boink": modules.Boink(),
    "hema": modules.Hema(),
    "tiya": modules.Tiya(),
    "paul": modules.Paul(),
    "paulraj": modules.Paulraj(),
}
system_responses = {
    "welcome": modules.Welcome(),
}

F_PATTERN = re.compile("can i get an? (.+) in the chat", flags=re.IGNORECASE | re.MULTILINE)


@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    group_id = message["group_id"]
    text = message["text"]
    name = message["name"]
    forename = name.split(" ", 1)[0]
    print("Message received: %s" % message)
    matches = F_PATTERN.search(text)
    if matches is not None and len(matches.groups()):
        reply(matches.groups()[0] + " ❤", group_id)
    if message["sender_type"] != "bot":
        if text.startswith(PREFIX):
            instructions = text[len(PREFIX):].strip().split(" ", 1)
            command = instructions.pop(0).lower()
            query = instructions[0] if len(instructions) > 0 else ""
            # Check if there's an automatic response for this command
            if command in static_commands:
                reply(static_commands[command], group_id)
            # If not, query appropriate module for a response
            elif command in commands:
                # Make sure there are enough arguments
                if len(list(filter(None, query.split("\n")))) < commands[command].ARGC:
                    reply("Not enough arguments!", group_id)
                else:
                    response = commands[command].response(query, message)
                    if response is not None:
                        reply(response, group_id)
            elif command == "help":
                if query:
                    query = query.strip(PREFIX)
                    if query in static_commands:
                        reply(PREFIX + query + ": static response.", group_id)
                    elif query in commands:
                        reply(PREFIX + query + ": " + commands[query].DESCRIPTION + f". Requires {commands[query].ARGC} argument(s).", group_id)
                    elif query in meme_commands:
                        reply(PREFIX + query + ": meme command; provide captions separated by newlines.", group_id)
                    else:
                        reply("No such command.", group_id)
                else:
                    help_string = "--- Help ---"
                    help_string += "\nStatic commands: " + ", ".join([PREFIX + title for title in static_commands])
                    help_string += "\nTools: " + ", ".join([PREFIX + title for title in commands])
                    help_string += f"\n(Run `{PREFIX}help commandname` for in-depth explanations.)"
                    reply(help_string, group_id)
            else:
                try:
                    closest = difflib.get_close_matches(command, list(static_commands.keys()) + list(commands.keys()), 1)[0]
                    advice = f"Perhaps you meant {PREFIX}{closest}? "
                except IndexError:
                    advice = ""
                reply(f"Command not found. {advice}Use !help to view a list of commands.", group_id)

        if "thank" in text.lower() and "harbot" in text.lower():
            reply("You're welcome, " + forename + "! :)", group_id)
    if message["system"]:
        for option in system_responses:
            if system_responses[option].RE.match(text):
                reply(system_responses[option].response(text, message), group_id)
        """
        if system_responses["welcome"].RE.match(text):
            check_names = system_responses["welcome"].get_names(text)
            for check_name in check_names:
                reply(commands["vet"].check_user(check_name), group_id)
        """
    return "ok", 200


def reply(message, group_id):
    """
    Reply in chat.
    :param message: text of message to send. May be a tuple with further data, or a list of messages.
    :param group_id: ID of group in which to send message.
    """
    # Recurse to send a list of messages.
    # This is useful when a module must respond with multiple messages.
    # TODO: This feels sort of clunky.
    if isinstance(message, list):
        for item in message:
            reply(item, group_id)
        return
    data = {
        "bot_id": GROUPS[group_id]["bot_id"],
    }
    if isinstance(message, tuple):
        text, image = message
    else:
        text = message
        image = None
    if len(text) > MAX_MESSAGE_LENGTH:
        # If text is too long for one message, split it up over several
        for block in [text[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]:
            reply(block, group_id)
        data["text"] = ""
    else:
        data["text"] = text
    if image is not None:
        data["picture_url"] = image
    # Prevent sending message if there's no content
    # It would be rejected anyway
    if data["text"] or data["picture_url"]:
        response = requests.post("https://api.groupme.com/v3/bots/post", data=data)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


def in_group(group_id):
    return db.session.query(db.exists().where(Bot.group_id == group_id)).scalar()



    return "ok", 200
