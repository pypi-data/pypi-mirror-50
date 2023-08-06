from sdk.utils.request_sender import RequestSender


class TestCase(RequestSender):
    url = "/api/test-case/"

    def __init__(self, debug=False, proxy=None):
        RequestSender.__init__(self, proxy=proxy, debug=debug)

    def post(self, token, name, execution_id, status, duration, failed_reason=None, **kwargs):
        headers = {
            "Authorization": "Bearer " + token,
        }
        data = {
            "name": name,
            "execution": execution_id,
            "status": status,
            "failed_reason": failed_reason,
            "duration": duration
        }
        return self.send(self.url, method="POST", headers=headers, data=data)

