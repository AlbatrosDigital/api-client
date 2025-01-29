import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shipyard-client",
    version="0.0.2",
    author="Erik Verboom",
    author_email="erik@albatros.digital",
    description="A client to access the AlbatrosDigital shipyard, building digital ships",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click',
        'gql',
        'plotly',
        'pyjwt',
        'aiohttp',
        'pandas',
        'numpy'
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'client = src.client:shipyard_client',
        ],
    },
)