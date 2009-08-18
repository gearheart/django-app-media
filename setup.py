from setuptools import setup, find_packages

setup(name="app_media",
           version="0.1",
           description="Django application to handle application media",
           author="Vladimir Sidorenko",
           author_email="yoyavova@gmail.com",
           packages=find_packages(),
           include_package_data=True,
)

