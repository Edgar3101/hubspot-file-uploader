import requests
from requests.adapters import HTTPAdapter, Retry


class ApiRequester(requests.Session):
    """
    A class representing an API requester with an API key and retry mechanism.

    Attributes:
        api_key (str): The API key to use for authentication.
        retry_attempts (int): The number of times to retry a failed request.
        url_base (str): The base URL for the API.
    """

    def __init__(self, api_key: str, retry_attempts: int = 3,  *args, **kwargs):
        """
        Initializes the ApiRequester with the given parameters.

        Args:
            url_base (str): The base URL for the API.
            api_key (str): The API key to use for authentication.
            retry_attempts (int, optional): The number of times to retry a failed request. Defaults to 3.
        """
        super().__init__(*args, **kwargs)
        self.url_base = "https://api.hubapi.com/files/v3/files"
        self.api_key = api_key
        self.retry_attempts = retry_attempts
        self._configure_session()

    def _configure_session(self) -> None:
        """
        Configures the session with the API key and retry mechanism.
        """
        self._add_api_key_to_headers()
        self._configure_retry()

    def _add_api_key_to_headers(self) -> None:
        """
        Adds the API key to the session headers.
        """
        self.headers.update({"Authorization": "Bearer " + self.api_key})

    def _configure_retry(self) -> None:
        """
        Configures the retry mechanism for the session.
        """
        retries = Retry(total=self.retry_attempts)
        self.mount("https://", HTTPAdapter(max_retries=retries))

    def request(self, method, url, params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,**kwargs):
        """
        Makes a request to the API with the given method and URL.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (str): The URL to make the request to. This should be a relative URL, as the base URL is already set in the class instance.
            **kwargs: Additional keyword arguments to pass to the requests.Session.request() method.

        Returns:
            requests.Response: The response object from the API request.
        """
        modified_url = self.url_base + url
        return super().request(method, modified_url, params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,**kwargs)