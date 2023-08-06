from setuptools import setup, find_packages

# read the contents of your README file
from os import path
with open(path.join(path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="devpi-auth-gitlab",
    description="An authentication plugin for use with gitlab-ci, utilising the build in registry token authentication scheme",
    long_description=long_description,
    author="Andrew Leech",
    author_email="andrew@alelec.net",
    url="https://gitlab.com/andrewleech/devpi-gitlab-auth",
    keywords="devpi plugin",
    entry_points={
        'devpi_server': [
            "devpi-auth-gitlab = devpi_auth_gitlab.main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'requests',
        'devpi-server>=2.0.0',
    ]
)
