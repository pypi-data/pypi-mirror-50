from sdk.execution import Execution
from sdk.testcase import TestCase
from sdk.authentication import Authentication


auth = Authentication()
token = auth.login("user1", "123")


exe = Execution(debug=False)
r = exe.post(token=token,
           project_id="23b79f25-5f6d-46d8-954d-5b4b014c5c3c",
           test_suite="suite1",
           )

tc = TestCase()
r = tc.post(token=token,
            name="tc01",
            execution_id=r.message['_id']['$oid'],
            status="passed",
            duration=12,
            )

print(r.status_code)
print(r.message)
