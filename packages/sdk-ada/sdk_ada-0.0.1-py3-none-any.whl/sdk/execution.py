from sdk.utils.request_sender import RequestSender


class Execution(RequestSender):
    url = "/api/execution/"

    def __init__(self, debug=False, proxy=None):
        RequestSender.__init__(self, proxy=proxy, debug=debug)

    def post(self, token, project_id, test_suite, total_test_cases=0):
        headers = {
            "Authorization": "Bearer " + token,
        }
        data = {
            "project_id": project_id,
            "test_suite": test_suite,
            "total_test_cases": total_test_cases,
        }
        return self.send(self.url, method="POST", headers=headers, data=data)

