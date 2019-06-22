from .base import Module

SOCK_URL = "https://www.mden.com/product/Navy/Yellow_Striped_Michigan_Socks?FOG6192+SEARCH"
SOCK_PRICE = 10.95


class Price(Module):
    DESCRIPTION = "Convert USD to UMS"
    ARGC = 1

    def response(self, query, message):
        query = query.strip().strip('$')
        price = float(query)
        return "For $%.2f, you could purchase %.2f pairs of socks from the M Den. Make the right choice here: %s" % (price, price / SOCK_PRICE, SOCK_URL)
