from os import path
from setuptools import setup, find_packages
import sys
import versioneer


# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (3, 6)
if sys.version_info < min_version:
    error = """
intake-bluesky does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(*sys.version_info[:2], *min_version)
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]


setup(
    name='intake-bluesky',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Bridge between intake and bluesky's event model",
    long_description=readme,
    author="Brookhaven National Lab",
    author_email='dallan@bnl.gov',
    url='https://github.com/NSLS-II/intake-bluesky',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            # 'command = some.module:some_function',
        ],
        'intake.drivers': [
            'bluesky-event-stream = intake_bluesky.core:BlueskyEventStream',
            'bluesky-jsonl-catalog = intake_bluesky.jsonl:BlueskyJSONLCatalog',
            ('bluesky-mongo-embedded-catalog = '
             'intake_bluesky.mongo_embedded:BlueskyMongoCatalog'),
            ('bluesky-mongo-normalized-catalog = '
             'intake_bluesky.mongo_normalized:BlueskyMongoCatalog'),
            'bluesky-msgpack-catalog = intake_bluesky.msgpack:BlueskyMsgpackCatalog',
            'bluesky-run = intake_bluesky.core:BlueskyRun',
        ]
    },
    include_package_data=True,
    package_data={
        'intake_bluesky': [
            # When adding files here, remember to update MANIFEST.in as well,
            # or else they will not be included in the distribution on PyPI!
            # 'path/to/data_file',
            ]
        },
    python_requires='>={}'.format('.'.join(str(n) for n in min_version)),
    install_requires=requirements,
    license="BSD (3-clause)",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
