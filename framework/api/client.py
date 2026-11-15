"""Thin HTTP client: one session, timeouts, retries, and every call logged to the Allure report."""

from __future__ import annotations

import json
import time

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ApiClient:
    def __init__(self, base_url: str, timeout: float = 15.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "User-Agent": "qa-automation-framework"})
        # Retry only transient infrastructure errors, never assertion-relevant 4xx responses.
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=(502, 503, 504), allowed_methods=None)
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        with allure.step(f"{method.upper()} {url}"):
            started = time.perf_counter()
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.elapsed_ms = round((time.perf_counter() - started) * 1000)  # type: ignore[attr-defined]
            self._attach(method, url, kwargs, response)
            return response

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    @staticmethod
    def _attach(method: str, url: str, kwargs: dict, response: requests.Response) -> None:
        body = kwargs.get("json")
        request_text = f"{method.upper()} {url}\n\n{json.dumps(body, indent=2) if body is not None else ''}"
        allure.attach(request_text, name="request", attachment_type=allure.attachment_type.TEXT)
        try:
            pretty = json.dumps(response.json(), indent=2)[:20000]
            kind = allure.attachment_type.JSON
        except ValueError:
            pretty, kind = response.text[:20000], allure.attachment_type.TEXT
        allure.attach(
            f"HTTP {response.status_code} ({getattr(response, 'elapsed_ms', '?')} ms)\n\n{pretty}"
            if kind is allure.attachment_type.TEXT
            else pretty,
            name=f"response {response.status_code}",
            attachment_type=kind,
        )
