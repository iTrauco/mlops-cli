from setuptools import setup, find_packages

setup(
    name="mlops_catalog",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "rich>=10.0",
        "pandas>=1.3",
        "pyyaml>=5.4",
        "sqlalchemy>=1.4",
        "typer>=0.4",
        "python-dotenv>=0.19",
    ],
    entry_points={
        "console_scripts": [
            "mlops=mlops_catalog.cli:app",
        ],
    },
)
