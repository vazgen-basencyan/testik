import boto3
from botocore.exceptions import NoCredentialsError


class AWSClient:
    def __init__(self, bucket_name=None, endpoint=None, access_key=None, secret_key=None):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', endpoint_url=endpoint, aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)

    def upload(self, file_path, object_for_upload=None):
        try:
            self.s3.upload_file(file_path, self.bucket_name, object_for_upload)
            print(f"File {file_path} uploaded to {object_for_upload} successfully.")
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except NoCredentialsError:
            print("Credentials not available.")

    def delete_folder(self, aws_path):
        folder_prefix = aws_path.split('/')[0]
        try:
            objects = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=folder_prefix)['Contents']

            for obj in objects:
                self.s3.delete_object(Bucket=self.bucket_name, Key=obj['Key'])

            print(f"Folder {self.bucket_name}/{folder_prefix} deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_bucket_content(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            objects = response.get('Contents', [])

            if objects:
                for obj in objects:
                    self.s3.delete_object(Bucket=self.bucket_name, Key=obj['Key'])
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_bucket(self):
        try:
            if self.bucket_name:
                self.s3.create_bucket(Bucket=self.bucket_name)
            else:
                print("Error: Bucket name not provided.")
        except Exception as e:
            print(f"Error creating bucket '{self.bucket_name}': {e}")

    def remove_bucket(self):
        try:
            if self.bucket_name:
                self.s3.delete_bucket(Bucket=self.bucket_name)
            else:
                print("Error: Bucket name not provided.")
        except Exception as e:
            print(f"Error deleting bucket '{self.bucket_name}': {e}")

    def set_bucket_name(self, bucket_name):
        self.bucket_name = bucket_name
