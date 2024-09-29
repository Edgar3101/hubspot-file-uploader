from abstract import AbstractFileCMS
import os, json


class FileCMS(AbstractFileCMS):
    """
    This FileCMS class interact with other classes to get data from the CMS, 
    to manage files and to send them to the CRM and the CMS.
    
    """

    def upload_file(self, **kwargs) -> None:
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
                self.make_request(data=data, files=files)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist.")
  

    def make_request(self, **kwargs) -> None:
        """
        Make a request to the CMS.

        Args:
            data (dict, optional): The data to send in the request body.
            file (dict, oprional): The file to send in the request body.
            json (dict, optional): The JSON data to send in the request body.
            url (string, required): The URL to send the request to.

        We can only pass data and file together or json alone.
        """
        

        data = kwargs.get("data")
        json = kwargs.get("json")
        files = kwargs.get("files")

        
  