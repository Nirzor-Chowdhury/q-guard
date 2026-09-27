from __future__ import annotations

import importlib.metadata
import platform
import ssl
import sys

PACKAGES = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "pydantic-settings",
    "sqlalchemy",
    "psycopg",
    "cryptography",
    "pytest",
]


def package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "NOT INSTALLED"


def main() -> None:
    print("Q-Guard environment check")
    print("=" * 30)
    print(f"Python:    {sys.version.split()[0]}")
    print(f"Platform:   {platform.platform()}")
    print(f"OpenSSL:    {ssl.OPENSSL_VERSION}")
    print()

    print("Python packages")
    print("-" * 30)

    for package in PACKAGES:
        print(f"{package}: {package_version(package)}")


if __name__ == "__main__":
    main()
