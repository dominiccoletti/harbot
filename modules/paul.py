from .base import Module
import tinytext


class Paul(Module):
    DESCRIPTION = "ᴾᵃᵘˡᵎ"
    ARGC = 1

    def response(self, query, message):
        return tinytext.tinytext(query)
