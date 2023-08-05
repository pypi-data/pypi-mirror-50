from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nginxcsp",
    version="0.1.0",
    description="Generate NGINX Content-Security-Policy headers from HTML \
    files",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "nginxcsp = nginxcsp.__main__:main"
        ]
    },

    author="Gian Ortiz",
    author_email="brksgian@gmail.com",

    url="https://github.com/GianOrtiz/nginxcsp",
    project_urls={
        "Source Code": "https://github.com/GianOrtiz/nginxcsp",
    },

    keywords="nginx config security",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
