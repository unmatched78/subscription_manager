from setuptools import setup, find_packages

setup(
    name="subscription_manager",
    version="0.1.0",
    description="Framework-agnostic subscription & trial management",
    author="viella",
    author_email="iradukundavierra4@gmail.com",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=2.0",
        "psycopg2-binary>=2.9"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)
