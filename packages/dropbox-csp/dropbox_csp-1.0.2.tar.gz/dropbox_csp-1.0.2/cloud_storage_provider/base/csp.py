import io

from abc import ABC, abstractmethod


class CloudStorageProvider(ABC):
	"""
		Abstract Class describing the common operations needed to be perfomed
		by a cloud storage provider with regards to:
		- Listing files available in a bucket
		- Upload files and folders to a bucket
		- Fetching files and folders from a bucket
	"""

	@abstractmethod
	def create_folder(self, target_path, folder_name):
		pass	

	@abstractmethod
	def upload_stream(self, file_stream: io.BytesIO, filename: str,
		folder: str, subfolder: str):
		pass

	@abstractmethod
	def list_files(self, folder_path):
		pass

	@abstractmethod
	def get_file(self, file_path):
		pass
