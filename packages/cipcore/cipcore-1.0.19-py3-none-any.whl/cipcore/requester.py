from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class CipSession(Session):
    ERRORS = (400, 403, 404, 500, 502, 503, 504)
    BACKOFF_FACTOR = 0.5

    def __init__(self, retries, **kwargs):
        super().__init__(**kwargs)

        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=self.BACKOFF_FACTOR,
            status_forcelist=self.ERRORS,
            raise_on_status=False
        )

        adapter = HTTPAdapter(max_retries=retry)
        self.mount('http://', adapter)
        self.mount('https://', adapter)
