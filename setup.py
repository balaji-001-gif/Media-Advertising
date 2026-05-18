from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

setup(
    name="media_advertising",
    version="0.0.1",
    description="Media & Advertising ERP for ERPNext v15+",
    author="Your Company",
    author_email="dev@yourcompany.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
