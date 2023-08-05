from setuptools import setup, find_packages

DESC = "PanaceaMobile \"API\" implementation in Python"

version_file = open("PanaceaMobile/const.py")
VERSION = None
for c in version_file.readlines():
    c = c.strip()
    if not c.startswith("VERSION"):
        continue
    key, val = c.split('=')
    VERSION = val.strip().split('"')[1]

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()

setup(
    name='PanaceaMobile',
    version=VERSION,
    description=DESC,
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/jargij/panaceamobile-python',
    author='Jacek Smit',
    author_email='info@jaceksmit.nl',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Communications :: Telephony',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    platforms='any',
    keywords=['SMS', 'PanaceaMobile', 'messaging'],
    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip
    install_requires=['requests'],
    python_requires='>=3.5'
)
