from .base import Module


class Paulraj(Module):
    DESCRIPTION = "PUTS! AN! EXCLAMATION! POINT! BETWEEN! EACH! WORD!"

    def paulrajify(self, word):
        return word + "!"

    def response(self, query, message):
        return " ".join([self.paulrajify(word) for word in query.split(" ")])
