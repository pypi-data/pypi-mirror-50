
from promium.elements.input_field import InputField
from promium.waits import wait_for_page_loaded


class UploadButton(InputField):

    def upload_file(self, file_path):
        """Uploads file by file path"""
        self.send_keys(file_path)
        wait_for_page_loaded(self.driver)
