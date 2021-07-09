import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

DEFAULT_TIMEOUT = 5 # seconds

STATUS_TO_RETRY_ON = [
    429, 500, 502, 503, 405
]

TOTAL_RETRIES = 3

BACKOFF_FACTOR = 1 # seconds

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

retries = Retry(
    total=TOTAL_RETRIES, backoff_factor=BACKOFF_FACTOR, allowed_methods=None, status_forcelist=STATUS_TO_RETRY_ON)

http = requests.Session()
http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))

