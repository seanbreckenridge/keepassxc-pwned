import time
import responses

from keepassxc_pwned import check_password, PwnedPasswordException

from .common import *

@vcr.use_cassette("tests/vcr_cassettes/check_password.yaml")
def test_check_password():
    count = check_password(passwd="password")
    assert count == 3730471
    time.sleep(2)


def test_lookup_pwned_user_error():
    with pytest.raises(ValueError) as user_error:
        check_password(passwd = None, pw_hash = None)
        assert str(user_error) == "You must pass either 'passwd' or 'pw_hash'"


@responses.activate
def test_no_user_agent():
    api_url = "https://api.pwnedpasswords.com/range/5BAA6"
    responses.add(responses.GET, api_url,
                  json={'error': 'no user agent'}, status=403)
    with pytest.raises(PwnedPasswordException) as no_user_agent:
        check_password("password")
    assert no_user_agent.value.status_code == 403
    assert no_user_agent.value.url == api_url
    assert len(responses.calls) == 1


