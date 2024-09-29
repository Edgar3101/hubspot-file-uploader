from api_requester import ApiRequester
from files.filecms import FileCMS

class HubSpot:
    """
    Class to interact with the HubSpot API.
    
    Attributes:
        __api_key: API key for authentication.
        __retry: Number of retries in case of failure.
    """
    def __init__(self, api_key: str, retry: int = 3):
        """
        Initializes the HubSpot class.

        Args:
            api_key (str): The API key for authentication.
            retry (int): The number of retry attempts in case of failure.
        """
        self.__validate_params(api_key, retry)
        self.__api_key = api_key
        self.__retry = retry
        self.__requester = ApiRequester(self.__api_key, self.retry)
        
    def __validate_params(self, api_key: str, retry: int) -> None:
        """Validates the input parameters."""
        if not isinstance(api_key, str):
            raise ValueError("The 'api_key' parameter must be a string.")
        if not isinstance(retry, int):
            raise ValueError("The 'retry' parameter must be an integer.")

    @property
    def api_key(self) -> str:
        """Returns a partial version of the API key."""
        return f"The provided API key is: {self.__api_key[0:5]}..."

    @property
    def retry(self) -> int:
        """Returns the configured retry count."""
        return self.__retry

    @classmethod
    def create(cls, api_key: str, retry: int = 3) -> 'HubSpot':
        """Creates a new instance of HubSpot."""
        return cls(api_key, retry)
    
    @property
    def file_cms(self) -> 'FileCMS':
        """Creates a new instance of FileCMS."""
        return FileCMS(self, self.__requester)
