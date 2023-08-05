import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webcubers",
    version="1.5",
    author="WebCubers",
    author_email="python@webcubers.com",
    description="webcubers python interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/webcubers/webcubers-pypi",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'appdirs',
        'cutie'
    ],
    entry_points = {
        'console_scripts': ['cubers=webcubers.cubers:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)