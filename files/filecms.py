from abstract import AbstractFileCMS


class FileCMS(AbstractFileCMS):
    """
    This FileCMS class interact with other classes to get data from the CMS, 
    to manage files and to send them to the CRM and the CMS.
    
    """

    def upload_file(self, **kwargs) -> None:
        """
        Upload a file to the CMS.
        """
        pass

    def make_request(self, **kwargs) -> None:
        """
        Make a request to the CMS.
        """
        pass
  