import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mld",
    version="0.0.2",
    author="romanjoffee",
    author_email="rjugai@curematch.com",
    description="Package to support MLD",
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
    packages=setuptools.find_packages(),
    url="https://curematch.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["psycopg2-binary==2.8.3", "click==7.0"],
    entry_points={
        "console_scripts": [
            "mld=scripts.cli:cli"
        ]
    },
    include_package_data=False
)
