from .abstract_hubspot_client import AbstractHubspot
from requests import Session

class AbstractFileCMS:
    """
    This FileCMS class interact with other classes to get data from the CMS, 
    to manage files and to send them to the CRM and the CMS.
    
    Attributes:
        __hubspot_instance: Instance of the HubSpot class.
        __requester: Instance of the ApiRequester class.
    """
    def __init__(self, hubspot_instance: AbstractHubspot, requester: Session):
        """
        self.__hubspot_instance = hubspot_instance
        """
        self.__requester = requester
        self.__hubspot_instance = hubspot_instance
    
    @property
    def requester(self) -> Session:
        """
        Returns the requester instance.
        """
        return self.__requester
    
    @property
    def hubspot_instance(self) -> AbstractHubspot:
        """
        Returns the hubspot instance.
        """
        return self.__hubspot_instance  
