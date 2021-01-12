from setuptools import setup, find_namespace_packages

setup(
    name='zowe_core_for_zowe_sdk',
    version='0.0.5',
    description='Zowe Python SDK - Core package',
    url="https://github.com/zowe/zowe-client-python-sdk",
    author="Guilherme Cartier",
    author_email="gcartier94@gmail.com",
    license="EPL-2.0",
    classifiers=[
        "Programming Language :: Python :: 3"],
    install_requires=['requests', 'urllib3', 'pyyaml'],
    packages=find_namespace_packages(include=['zowe.*'])
)
