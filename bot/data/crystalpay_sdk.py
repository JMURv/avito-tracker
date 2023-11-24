import requests
import json


class InvoiceType:
    topup = "topup"
    purchase = "purchase"


class PayoffSubtractFrom:
    balance = "balance"
    amount = "amount"


class crystal_utils:
    ''' Дополнительный класс, содержащий в себе дополнительные функции для работы SDK '''

    ''' Соединяет необязательные параметры с обязательными '''

    def concatParams(self, concatList, kwargs):

        temp = concatList

        for key, param in kwargs:
            temp[key] = param

        return temp

    ''' Отправка запроса на API '''

    def requestsApi(self, method, function, params):

        response = json.loads(
            requests.post(
                f"https://api.crystalpay.io/v2/{method}/{function}/",
                data=params,
                headers={'Content-Type': 'application/json'}
            ).text
        )

        if (response["error"]):
            raise Exception(response['errors'])

        ''' Убираем из JSON ответа сообщения об ошибках '''

        del response["error"]
        del response["errors"]

        return response


class CrystalPAY:
    ''' Гланый класс для работы с CrystalApi '''

    def __init__(self, auth_login, auth_secret, salt):
        ''' Создание подклассов '''

        self.Me = self.Me(auth_login, auth_secret, crystal_utils())
        self.Invoice = self.Invoice(auth_login, auth_secret, crystal_utils())

    class Me:

        def __init__(self, auth_login, auth_secret, crystal_utils):
            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        ''' Получение информации о кассе '''

        def getinfo(self):
            response = self.__crystal_utils.requestsApi(
                "me",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret
                })
            )

            return response

    class Invoice:

        def __init__(self, auth_login, auth_secret, crystal_utils):
            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        ''' Получение информации о счёте '''

        def getinfo(self, id):
            response = self.__crystal_utils.requestsApi(
                "invoice",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "id": id
                })
            )

            return response

        ''' Выставление счёта на оплату '''

        def create(self, amount, type_, lifetime, **kwargs):
            response = self.__crystal_utils.requestsApi(
                "invoice",
                "create",
                json.dumps(
                    self.__crystal_utils.concatParams(
                        {
                            "auth_login": self.__auth_login,
                            "auth_secret": self.__auth_secret,
                            "amount": amount,
                            "type": type_,
                            "lifetime": lifetime
                        },
                        kwargs.items()
                    )
                )
            )

            return response
