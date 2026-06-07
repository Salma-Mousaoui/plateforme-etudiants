from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class ListingsStorage(S3Boto3Storage):
    bucket_name = 'listings'
    querystring_auth = False
    file_overwrite = False
    default_acl = 'public-read'

    @property
    def custom_domain(self):
        return (
            f"{settings.SUPABASE_PROJECT_REF}"
            f".supabase.co/storage/v1/object/public/listings"
        )


class ProfilesStorage(S3Boto3Storage):
    bucket_name = 'profiles'
    querystring_auth = False
    file_overwrite = False
    default_acl = 'public-read'

    @property
    def custom_domain(self):
        return (
            f"{settings.SUPABASE_PROJECT_REF}"
            f".supabase.co/storage/v1/object/public/profiles"
        )


class ChatStorage(S3Boto3Storage):
    bucket_name = 'chat'
    querystring_auth = False
    file_overwrite = False
    default_acl = 'public-read'

    @property
    def custom_domain(self):
        return (
            f"{settings.SUPABASE_PROJECT_REF}"
            f".supabase.co/storage/v1/object/public/chat"
        )
