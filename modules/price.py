from .base import Module

SOCK_URL = "https://columbia.bncollege.com/webapp/wcs/stores/servlet/SubcategoryView?sortOption=2&results=113&plus=0&narrowByPrice=0&pageToDisplay=1&sortOptionName=Price+%3A+High+to+low&subCatTotalCount=&level=&catalogId=10001&parentSubCatIdFlag=true&parentCatId=40360&langId=-1&categoryId=40403&topCatId=40000&storeId=10053&compareIds="
SOCK_PRICE = 12.98


class Price(Module):
    DESCRIPTION = "Convert USD to CSK"
    ARGC = 1

    def response(self, query, message):
        query = query.strip().strip('$')
        price = float(query)
        return "For $%.2f, you could purchase %.2f pairs of socks from the Columbia Bookstore. Make the right choice here: %s" % (price, price / SOCK_PRICE, SOCK_URL)
