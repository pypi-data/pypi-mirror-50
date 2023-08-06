from setuptools import setup, find_packages
from os.path import join, dirname


VERSION = __import__('fake_usrag_bor').__version__

setup(
    name='fake_usrag_bor',
    version=VERSION,
    author='oskarmenrus',
    author_email='oskarmenrus@gmail.com',
    url='https://github.com/oskarmenrus',
    description='Simple package with fake user agents for your requests.',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['.idea']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        'user', 'agent', 'user agent', 'useragent',
        'fake', 'fake useragent', 'fake user agent',
    ],
)
