from .abstract import AbstractFileCMS
from requests import HTTPError, Response
import logging


class FileCMS(AbstractFileCMS):
    """
    This FileCMS class interact with other classes to get data from the CMS, 
    to manage files and to send them to the CRM and the CMS.
    
    """

    def upload_file(self, **kwargs) -> Response | None:
        """
        Uploads a file to the CMS.

        Args:
            file_path (str): The path to the file to upload. Required.
            folder_path (str, optional): The path to the destination folder. 
                Mutually exclusive with `folder_id`.
            folder_id (str, optional): The ID of the destination folder.
                Mutually exclusive with `folder_path`.
            file_name (str, optional): The name of the file on the CMS. 
                Defaults to the original file name.
            options (dict, optional): Additional upload options. 
                Defaults to an empty dictionary. Example: {"access": "PRIVATE"}.

        Raises:
            ValueError: If required arguments are missing or mutually 
                exclusive arguments are provided together.
            TypeError: If `options` is not a dictionary.
            FileNotFoundError: If the specified file does not exist.
        """
        
        required_args = ["file_path", "folder_path", "options"]
        missed_args = [x for x in required_args if x not in kwargs.keys()]
        if missed_args:
            raise ValueError(f"Missing required arguments: {', '.join(missed_args)}")

        file_path = kwargs.get("file_path")
        folder_path = kwargs.get("folder_path")
        options = kwargs.get("options", {})
        file_name = kwargs.get("file_name", os.path.basename(file_path)) # type: ignore
        folder_id = kwargs.get("folder_id")

        if folder_id and folder_path:
            raise ValueError("You can't provide both folder_id and folder_path")
        if not isinstance(options, dict):
            raise TypeError("options args must be a dict")
    
        data = {"options": options, "file_name": file_name}
        if folder_id:
            data["folderId"] = folder_id
        if folder_path:
            data["folderPath"] = folder_path

        # We create our file dict
        try:
            with open(file_path, "rb") as f: # type: ignore
                files = {"file": f}
                return self.make_request(url="/",data=data, files=files)
        except FileNotFoundError as e:
            logging.error(f"The file {file_path} does not exist.")
        except HTTPError as e:
            logging.error(f"Error while uploading file: {e}")
            return None

    def delete_file(self, file_id: str) -> Response | None:
        """
        Deletes a file from the CMS.

        Args:
            file_id (str): The ID of the file to delete.

        Returns:
            Optional[Response]: The response from the File CMS API, or None if an error occurred.
        """
        if not file_id:
            raise ValueError("Missing 'file_id' argument")
        try:
            return self.make_request(url=f"/{file_id}", method="DELETE")
        except HTTPError as e:
            logging.error(f"Error while deleting file: {e}")
            return None
        

  

    def make_request(self, **kwargs) -> Response | None:
        """
        Make a request to the CMS.

        Args:
            data (dict, optional): The data to send in the request body.
            file (dict, oprional): The file to send in the request body.
            json (dict, optional): The JSON data to send in the request body.
            url (string, required): The URL to send the request to.
            params (dict, optional): if params is provided we should make a GET request
            method (str, optionl): if metehod is provided we use the method

        We can only pass data and file together or json alone.
        Raises:
            ValueError: If both data/files and json are provided together or URL is missing
            TypeError: If any of the arguments are of the wrong type.
            HTTPError: If the request to the CMS fails.

        Returns:
            Response: The response from the CMS.
        """
        

        data = kwargs.get("data")
        json = kwargs.get("json")
        files = kwargs.get("files")
        url= kwargs.get("url")
        params = kwargs.get("params")
        method = kwargs.get("method")

        if url is None:
            raise ValueError("Missing `url` argument")
        if data or files and json:
            raise ValueError("You can't provide both data and json")
          
        if method == "GET" or method == "DELETE":
            response = self.requester.request(method=method, url=kwargs["url"], params=params)
        elif method == "POST" or method == "PUT" or method == "PATCH":
            if json:
                response = self.requester.request(method=method, url=kwargs["url"], json=json)
            elif data or files:
                response = self.requester.request(method=method, url=kwargs["url"], data=data, files=files)
            else:
                raise ValueError("Either 'json' or 'data'/'files' must be provided")
        else:
            raise ValueError("Invalid method. Supported methods are 'GET', 'POST', 'PUT', 'PATCH', and 'DELETE'.")

        return response
        

        


        
  