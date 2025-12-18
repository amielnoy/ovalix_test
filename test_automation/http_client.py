import os
import requests


class HttpClient:
    def __init__(self, base_url: str | None = None, timeout: int = 10):
        self.base_url = base_url or os.getenv("API_BASE_URL")
        if not self.base_url:
            raise RuntimeError("API_BASE_URL not set")
        self.session = requests.Session()
        self.timeout = timeout

    def _url(self, path: str | None) -> str:
        if not path:
            # ensure base URL ends with a slash so POSTs to the collection
            # don't get redirected by Django's APPEND_SLASH middleware
            return self.base_url.rstrip('/') + '/'
        if path.startswith('http://') or path.startswith('https://'):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get(self, path: str = '', **kwargs):
        return self.session.get(self._url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str = '', **kwargs):
        return self.session.post(self._url(path), timeout=self.timeout, **kwargs)

    def put(self, path: str = '', **kwargs):
        return self.session.put(self._url(path), timeout=self.timeout, **kwargs)

    def delete(self, path: str = '', **kwargs):
        return self.session.delete(self._url(path), timeout=self.timeout, **kwargs)
