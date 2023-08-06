from sdk.utils.request_sender import RequestSender


class Authentication(RequestSender):
    url_login = "/api/user/login/"

    def __init__(self, debug=False, proxy=None):
        RequestSender.__init__(self, proxy=proxy, debug=debug)

    def login(self, username, password):
        data = {
            "username": username,
            "password": password
        }
        response = self.send(self.url_login, method="POST", data=data)
        return response.message['access']
