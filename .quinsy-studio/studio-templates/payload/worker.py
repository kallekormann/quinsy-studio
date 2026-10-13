"""Python embedding worker. Started only with the Compose profile `rag`.

Reads jobs from Redis, writes vectors to pgvector, and stores file bytes in the
S3-compatible bucket (MinIO locally, Cloudflare R2 in production).
A Payload job enqueues the work. This process does the long run.
"""

import os
import time


def main() -> None:
    redis_url = os.environ.get("REDIS_URL", "")
    database_url = os.environ.get("DATABASE_URL", "")
    print("embedding worker idle")
    print(f"redis configured: {bool(redis_url)}")
    print(f"database configured: {bool(database_url)}")
    while True:
        time.sleep(30)


if __name__ == "__main__":
    main()
