import vcr
import responses

from keepassxc_pwned import check_password, PwnedPasswordException

from .common import *

vcr_dir = os.path.join(this_dir, "vcr_cassettes")


@vcr.use_cassette("tests/vcr_cassettes/check_password.yaml")
def test_check_password():
    count = check_password(passwd="password")
    assert count == 3730471


def test_lookup_pwned_user_error():
    with pytest.raises(ValueError) as user_error:
        check_password(passwd=None, pw_hash=None)
    assert str(
        user_error.value) == "You must pass either 'passwd' or 'pw_hash'"


@responses.activate
def test_no_user_agent():
    api_url = "https://api.pwnedpasswords.com/range/5BAA6"
    responses.add(responses.GET,
                  api_url,
                  json={"error": "no user agent"},
                  status=403)
    with pytest.raises(PwnedPasswordException) as no_user_agent:
        check_password("password")
    assert no_user_agent.value.status_code == 403
    assert no_user_agent.value.url == api_url
    assert len(responses.calls) == 1


@responses.activate
def test_hit_rate_limit():
    api_url = "https://api.pwnedpasswords.com/range/5BAA6"
    successful_response = os.path.join(vcr_dir,
                                       "pwned_passwords_api_response.txt")
    with open(successful_response, "r") as success:
        success_text = success.read()
    responses.add(responses.GET,
                  api_url,
                  body="error: exceeded rate limit",
                  status=429)
    responses.add(responses.GET, api_url, body=success_text, status=200)
    count = check_password("password")
    assert count == 3000000
