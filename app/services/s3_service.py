import boto3
from io import BytesIO
from app.config import settings

class S3Service:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    def download_file(self, bucket_name: str, key: str) -> BytesIO:
        file_obj = BytesIO()
        self.s3.download_fileobj(bucket_name, key, file_obj)
        file_obj.seek(0)
        return file_obj

s3_service = S3Service()
