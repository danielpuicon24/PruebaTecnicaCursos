import os

AWS_ACCESS_KEY_ID = "DO00ZQ8LB4AEURVCDCPG"
AWS_SECRET_ACCESS_KEY ="oeKgM+lNKdvcRGdumDML1h8+qeL22CcexJVX/hvNtpo"
AWS_STORAGE_BUCKET_NAME ="spacebdprueba"
AWS_S3_ENDPOINT_URL="https://nyc3.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl" : "max-age=86400",
}
AWS_LOCATION = "https://spacebdprueba.nyc3.digitaloceanspaces.com"
DEFAULT_FILE_STORAGE = "PruebaTecnica.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "PruebaTecnica.cdn.backends.StaticRootS3Boto3Storage"