import os

import boto3
import minty.infrastructure.mime_utils as mu
from botocore.client import Config
from minty import Base
from minty.exceptions import ConfigurationConflict


class S3Wrapper(Base):
    def __init__(self, filestore_config: list, base_directory: str):
        self.filestore_config = filestore_config

        try:
            self.location_name = self.filestore_config[0]["name"]
            self.bucket = self.filestore_config[0]["bucket"]
        except KeyError as error:
            raise ConfigurationConflict(
                "Invalid configuration for S3 found"
            ) from error

        self.endpoint_url = self.filestore_config[0].get("endpoint_url", None)
        self.region_name = self.filestore_config[0].get("region_name", None)
        self.addressing_style = self.filestore_config[0].get(
            "addressing_style", "auto"
        )
        self.access_id = self.filestore_config[0].get("access_id", None)
        self.access_key = self.filestore_config[0].get("access_key", None)
        self.base_directory = base_directory

    def _get_filename(self, uuid):
        return f"{self.base_directory}/{uuid}"

    def upload(self, file_handle, uuid):
        timer = self.statsd.get_timer("file_upload")
        with timer.time("s3_upload"):
            boto_parameters = {}

            # If access id and key are not specified, boto3 will default to use
            # the EC2 IAM role, which is what we want on production.
            if self.access_id is not None and self.access_key is not None:
                boto_parameters["aws_access_key_id"] = self.access_id
                boto_parameters["aws_secret_access_key"] = self.access_key

            if self.endpoint_url is not None:
                boto_parameters["endpoint_url"] = self.endpoint_url

            if self.region_name is not None:
                boto_parameters["region_name"] = self.region_name

            s3_client = boto3.session.Session().client(
                service_name="s3",
                config=Config(
                    s3={
                        "addressing_style": self.addressing_style,
                        # "signature_version": signature_version,
                    }
                ),
                **boto_parameters,
            )
            response_dict = s3_client.put_object(
                Body=file_handle,
                Bucket=self.bucket,
                Key=self._get_filename(uuid),
            )

        file_handle.seek(0, os.SEEK_END)
        total_size = file_handle.tell()

        return {
            "uuid": uuid,
            "md5": response_dict["ETag"][1:-1],
            "size": total_size,
            "mime_type": mu.get_mime_type_from_handle(file_handle),
            "storage_location": self.location_name,
        }


class S3Infrastructure(Base):
    """Infrastructure Class for S3 Connection."""

    def __call__(self, config):
        """Create a new S3 connection using the specified configuration

        :param config: The configuration params necessary to connect to a S3 bucket.
        :return: A S3 handle for a bucket on a connection to an S3 server.
        :rtype: S3Wrapper
        """

        try:
            directory = config["storage_bucket"]
        except KeyError:
            try:
                directory = config["instance_uuid"]
            except KeyError as k:
                raise ConfigurationConflict(
                    "No instance UUID or storage bucket specified for S3 configuration"
                ) from k

        try:
            filestore_config = config["filestore"]
            if type(filestore_config) is not list:
                filestore_config = [filestore_config]
        except KeyError as error:
            raise ConfigurationConflict(
                "Invalid configuration for S3 found"
            ) from error

        return S3Wrapper(
            filestore_config=filestore_config, base_directory=directory
        )
