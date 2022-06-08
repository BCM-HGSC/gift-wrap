from requests import Session
from requests.adapters import HTTPAdapter  # pylint: disable=unused-import
from urllib3.util.retry import Retry


DEFAULT_TIMEOUT = 10  # seconds

STATUS_TO_RETRY_ON = [429, 502, 503, 405]

TOTAL_RETRIES = 3

BACKOFF_FACTOR = 2  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    """Adds Timeout to HTTPAdapater"""

    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    # pylint: disable=too-many-arguments
    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        return super().send(
            request, stream, timeout or self.timeout, verify, cert, proxies
        )


retries = Retry(
    total=TOTAL_RETRIES,
    backoff_factor=BACKOFF_FACTOR,
    allowed_methods=None,
    status_forcelist=STATUS_TO_RETRY_ON,
)

http = Session()
assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
http.hooks["response"] = [assert_status_hook]
http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
