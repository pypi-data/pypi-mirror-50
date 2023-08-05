import setuptools
import json

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('Pipfile.lock') as fd:
    lock_data = json.load(fd)
    install_requires = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['default'].items()
    ]
    tests_require = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['develop'].items()
    ]

setuptools.setup(
    name="panamah-sdk-python",
    version="1.0.1",
    author="Casa Magalhães",
    author_email="contato@casamagalhaes.com.br",
    description="Panamah Software Development Kit for Python",
    long_description="APIs and models for Panamah services",
    long_description_content_type="text/markdown",
    url="https://github.com/casamagalhaes/panamah-sdk-python",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)