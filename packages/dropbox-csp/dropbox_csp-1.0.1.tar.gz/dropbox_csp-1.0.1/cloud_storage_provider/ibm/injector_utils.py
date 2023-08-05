import ibm_boto3
from ibm_botocore.client import Config

from . import constants


def get_ibm_cos_client():
	# Create client connection
	cos_client = ibm_boto3.client("s3",
		ibm_api_key_id=constants.COS_API_KEY_ID,
		ibm_service_instance_id=constants.COS_RESOURCE_CRN,
		ibm_auth_endpoint=constants.COS_AUTH_ENDPOINT,
		config=Config(signature_version="oauth"),
		endpoint_url=constants.COS_ENDPOINT
	)

	return cos_client

def get_ibm_cos_resource():
	# Create resource connection
	cos_resource = ibm_boto3.resource("s3",
		ibm_api_key_id=constants.COS_API_KEY_ID,
		ibm_service_instance_id=constants.COS_RESOURCE_CRN,
		ibm_auth_endpoint=constants.COS_AUTH_ENDPOINT,
		config=Config(signature_version="oauth"),
		endpoint_url=constants.COS_ENDPOINT)

	return cos_resource