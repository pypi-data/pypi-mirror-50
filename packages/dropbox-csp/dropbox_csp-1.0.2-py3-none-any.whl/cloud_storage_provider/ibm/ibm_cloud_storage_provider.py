import ibm_boto3
from ibm_botocore.client import ClientError

from cloud_storage_provider.base.csp import CloudStorageProvider
from . import constants
from cloud_storage_provider.utils import get_logger
from . import injector_utils


class IBMCloudStorageProvider(CloudStorageProvider):

	def __init__(self, bucket_name, cos_client, cos_resource):
		# Setup a logger
		self.logger = get_logger()

		self.cos_resource = cos_resource
		self.cos_client = cos_client
		self.bucket_name = bucket_name	

		# create bucket (non-fatal fail if already exists)
		self.create_bucket(self.bucket_name)

	def create_bucket(self, bucket_name):
		self.logger.info("Creating new bucket: {0}".format(bucket_name))
		try:
			self.cos_resource.Bucket(bucket_name).create(
				CreateBucketConfiguration={
					"LocationConstraint": constants.COS_BUCKET_LOCATION
				}
			)
			self.logger.info("Bucket: {0} created!".format(bucket_name))
		except ClientError as be:
			self.logger.error("{0}\n".format(be))
		except Exception as e:
			self.logger.error("Unable to create bucket: {0}".format(e))
	
	def get_buckets(self):
		self.logger.info("Retrieving list of buckets")

		try:
			buckets = self.cos_resource.buckets.all()
			return buckets
		except ClientError as be:
			self.logger.error("{0}\n".format(be))
		except Exception as e:
			self.logger.error("Unable to retrieve list buckets: {0}".format(e))

		return None

	def upload_object(self, file_path):
		item_name = file_path.split("/")[-1]

		self.logger.info("Starting large file upload for {0} to bucket: {1}".format(
			item_name, self.bucket_name))

		# set the chunk size to 5 MB
		part_size = 1024 * 1024 * 5

		# set threadhold to 5 MB
		file_threshold = 1024 * 1024 * 5

		# set the transfer threshold and chunk size in config settings
		transfer_config = ibm_boto3.s3.transfer.TransferConfig(
			multipart_threshold=file_threshold,
			multipart_chunksize=part_size
		)

		# create transfer manager
		transfer_mgr = ibm_boto3.s3.transfer.TransferManager(self.cos_client, config=transfer_config)

		try:
			# initiate file upload
			future = transfer_mgr.upload(file_path, self.bucket_name, item_name)

			# wait for upload to complete
			future.result()

			self.logger.info("Large file upload complete!")
		except Exception as e:
			self.logger.error("Unable to complete large file upload: {0}".format(e))
		finally:
			transfer_mgr.shutdown()

	def upload_objects(self, file_paths):
		for file_path in file_paths:
			self.upload_object(file_path)

	def get_bucket_contents_v2(self, max_keys=50):
		object_names = []

		self.logger.info("Retrieving bucket contents from: {0}"
			.format(self.bucket_name))
		try:
			more_results = True
			next_token = ""

			while (more_results):
				response = self.cos_client.list_objects_v2(
					Bucket=self.bucket_name,
					MaxKeys=max_keys,
					ContinuationToken=next_token
				)

				files = response["Contents"]
				for file in files:
					self.logger.info("Item: {0} ({1} bytes).".format(file["Key"], file["Size"]))
					object_names.append(file["Key"])

				if (response["IsTruncated"]):
					next_token = response["NextContinuationToken"]
					self.logger.info("...More results in next batch!\n")
				else:
					more_results = False
					next_token = ""

			self.logger.info("Obtained contents of {}".format(self.bucket_name))
		except ClientError as be:
			self.logger.error("{0}\n".format(be))
		except Exception as e:
			self.logger.error("Unable to retrieve bucket contents: {0}".format(e))

		return object_names

	def list_objects(self):
		object_names = self.get_bucket_contents_v2()
		return object_names

	def get_item(self, item_name):
		file = None

		self.logger.info("Retrieving item from bucket: {0}, key: {1}"
			.format(self.bucket_name, item_name))
		try:
			file = self.cos_resource.Object(self.bucket_name, item_name).get()
		except ClientError as be:
			self.logger.error("{0}\n".format(be))
		except Exception as e:
			self.logger.error("Unable to retrieve file contents: {0}".format(e))

		return file

	def read_object(self, object_file):
		contents = None
		if object_file:
			contents = object_file["Body"].read()

		return contents

	def get_object(self, object_name):
		file = self.get_item(object_name)
		return file


def main():
	bucket_name = "jkuat-research-data"

	ibm = IBMCloudStorageProvider(
		bucket_name,
		injector_utils.get_ibm_cos_client(),
		injector_utils.get_ibm_cos_resource()
	)


if __name__ == "__main__":
	main()
