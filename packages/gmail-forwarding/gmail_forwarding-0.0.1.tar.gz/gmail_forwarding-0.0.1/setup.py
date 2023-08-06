from setuptools import setup
from os import path

DIR = path.dirname(path.abspath(__file__))

DESCRIPTION = "Automatic Forwarding of Selected Emails using Gmail API - with Subscription"

AUTHOR = 'FrenchCommando'

URL = 'https://github.com/FrenchCommando/gmail-forwarding'

EMAIL = 'martialren@gmail.com'

with open(path.join(DIR, 'requirements.txt')) as f:
    INSTALL_PACKAGES = f.read().splitlines()

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

# get __version__ from _version.py
ver_file = path.join('gmail_forwarding', '_version.py')
with open(ver_file) as f:
    exec(f.read())

VERSION = __version__

setup(
    name='gmail_forwarding',
    packages=['gmail_forwarding'],
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_PACKAGES,
    version=VERSION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    keywords=['gmail-api', 'subscription', 'forwarding'],
    python_requires='>=3',
    classifiers=[
                  "Programming Language :: Python :: 3.7",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
              ],
    scripts=['bin/gmail_forwarding_one_shot_main',
             'bin/gmail_forwarding_server_main']
)
