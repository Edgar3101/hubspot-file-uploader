import requests
from requests.adapters import HTTPAdapter, Retry
from dataclasses import dataclass

@dataclass
class ApiRequester:
    """
    A class representing an API requester with an API key and retry mechanism.

    Attributes:
        api_key (str): The API key to use for authentication.
        retry_attempts (int): The number of times to retry a failed request.
    """

    api_key: str
    retry_attempts: int

    def create_session(self) -> requests.Session:
        """
        Creates a requests Session instance with the provided API key and retry mechanism.

        Returns:
            requests.Session: A Session instance with the API key and retry mechanism configured.
        """
        # Create a new requests Session instance
        session = requests.Session()
        
        # Add the API key to the session headers
        self._add_api_key_to_headers(session)
        
        # Configure the retry mechanism for the session
        self._configure_retry(session)
        
        return session

    def _add_api_key_to_headers(self, session: requests.Session) -> None:
        """
        Adds the API key to the session headers.
        """
        session.headers.update({"Authorization": "Bearer " + self.api_key})

    def _configure_retry(self, session: requests.Session) -> None:
        """
        Configures the retry mechanism for the session.
        """
        retries = Retry(total=self.retry_attempts)
        session.mount("https://", HTTPAdapter(max_retries=retries))