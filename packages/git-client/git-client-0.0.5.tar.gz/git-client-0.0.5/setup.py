import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git-client",
    version="0.0.5",
    author="Andy Klier",
    author_email="andyklier@gmail.com",
    description="`git-client` or `gc` hopes to be an easy to use command line client for using git.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shindagger/git-client",
    packages=['gitclient'],
    include_package_data=True,
    install_requires= ['setuptools', 'inquirer'],
    entry_points = {
        'console_scripts': ['git-client=gitclient.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
