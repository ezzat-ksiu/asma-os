"""Cloudflare R2 adapter using the S3-compatible boto3 API."""
from __future__ import annotations

import os


class CloudflareR2Adapter:
    def __init__(self, *, account_id: str | None = None, access_key_id: str | None = None,
                 secret_access_key: str | None = None, client=None, region: str = "auto"):
        self.account_id = account_id or os.getenv("CLOUDFLARE_R2_ACCOUNT_ID")
        key = access_key_id or os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
        secret = secret_access_key or os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
        if client is not None:
            self.client = client
        else:
            if not all((self.account_id, key, secret)):
                raise ValueError("R2 account id and access credentials are required")
            try:
                import boto3
            except ImportError as exc:
                raise RuntimeError("Install boto3 to use Cloudflare R2") from exc
            self.client = boto3.client("s3", endpoint_url=f"https://{self.account_id}.r2.cloudflarestorage.com",
                aws_access_key_id=key, aws_secret_access_key=secret, region_name=region)

    def upload_asset(self, bucket: str, key: str, data: bytes, *, content_type: str,
                     metadata: dict[str, str] | None = None) -> dict:
        if not bucket or not key or not isinstance(data, bytes):
            raise ValueError("bucket, key, and byte content are required")
        self.client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type,
                               Metadata=metadata or {})
        return {"bucket": bucket, "key": key, "content_type": content_type, "bytes": len(data)}

    def configure_lifecycle(self, bucket: str, *, prefix: str, expiration_days: int) -> dict:
        if not prefix or expiration_days < 1:
            raise ValueError("a non-empty prefix and positive expiration are required")
        config = {"Rules": [{"ID": "asma-managed-expiration", "Status": "Enabled",
                             "Filter": {"Prefix": prefix}, "Expiration": {"Days": expiration_days}}]}
        self.client.put_bucket_lifecycle_configuration(Bucket=bucket, LifecycleConfiguration=config)
        return config

    def purge_prefix(self, bucket: str, prefix: str) -> int:
        if not bucket or not prefix or prefix in ("/", "*"):
            raise ValueError("privacy purge requires a specific non-empty prefix")
        paginator = self.client.get_paginator("list_objects_v2")
        removed = 0
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            objects = [{"Key": item["Key"]} for item in page.get("Contents", [])]
            if objects:
                self.client.delete_objects(Bucket=bucket, Delete={"Objects": objects, "Quiet": True})
                removed += len(objects)
        return removed
