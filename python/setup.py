from setuptools import setup, find_packages

setup(
    name="subscription_manager",
    version="0.1.0",
    description="Framework-agnostic subscription & trial management",
    author="Your Name",
    author_email="iradukundavierra4@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "SQLAlchemy>=2.0",
        "psycopg2-binary>=2.9"
    ],
    python_requires=">=3.9",
)
