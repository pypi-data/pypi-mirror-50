import io, os

import dropbox

from cloud_storage_provider.utils import get_logger
from cloud_storage_provider.base.csp import CloudStorageProvider


class DropBoxStorageProvider(CloudStorageProvider):

	def __init__(self, access_token):
		self.dbx = dropbox.Dropbox(access_token)
		self.logger = get_logger()

	def create_folder(self, target_path, folder_name):
		self.logger.info("Creating a folder at {} called {}".format(
			target_path, folder_name))

	def upload_stream(self, file_stream: io.BytesIO, filename: str,
		folder: str, subfolder: str, overwrite=False):

		if file_stream is None:
			raise TypeError("File stream cannot be None")
		if filename is None:
			raise TypeError("Must specify the file name")
		if folder is None:
			raise TypeError("Must specify folder path")

		data = file_stream.read()

		self.logger.debug("Creating a file with content {} at {} called {}".format(
			data, folder + subfolder, filename))

		# Use dropbox sdk to upload file to specified folder
		# Return the request response, or None in case of error.
		
		path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'),
			filename)

		while '//' in path:
			path = path.replace('//', '/')

		mode = (dropbox.files.WriteMode.overwrite
				if overwrite
				else dropbox.files.WriteMode.add)

		self.logger.debug("Using {} mode".format(mode))
		
		with file_stream:
			try:
				res = self.dbx.files_upload(
					data, path, mode,
					mute=True)
			except dropbox.exceptions.ApiError as err:
				self.logger.error('API Error: {}'.format(err))
				return None

		file_stream.close()
		
		self.logger.debug('Uploaded as: {}'.format(res.name.encode('utf8')))

		return res

	def list_files(self, folder: str, subfolder: str):
		self.logger.info("Listing files in folder {}".format(
			folder))

		path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))

		while '//' in path:
			path = path.replace('//', '/')
		path = path.rstrip('/')

		try:
			res = self.dbx.files_list_folder(path)
		except dropbox.exceptions.ApiError as err:
			self.logger.error('Folder listing failed for {} -- assumed empty: {}',
				path, err)
			return {}
		else:
			return res.entries

	def get_file(self, folder: str, subfolder: str, filename: str):
		self.logger.info("Fetching file {} at path {}".format(
			folder + subfolder,
			filename))

		path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'),
			filename)

		while '//' in path:
			path = path.replace('//', '/')
	
		try:
			md, res = self.dbx.files_download(path)
		except dropbox.exceptions.HttpError as http_err:
			self.logger.error('HTTP error: {}'.format(http_err))
			return None
		except dropbox.exceptions.ApiError as api_err:
			self.logger.error('API error: {}'.format(api_err))
			return None

		data = res.content

		return data

	def delete_file(self, folder: str, subfolder: str, filename: str):
		path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'),
			filename)

		while '//' in path:
			path = path.replace('//', '/')

		try:
			md, res = self.dbx.files_delete(path)
		except dropbox.exceptions.HttpError as http_err:
			self.logger.error('HTTP error: {}'.format(http_err))
		except dropbox.exceptions.ApiError as api_err:
			self.logger.error('API error: {}'.format(api_err))
