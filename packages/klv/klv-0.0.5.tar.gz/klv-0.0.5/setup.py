from setuptools import setup
from klv import __version__

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='klv',
    version=__version__,
    license='MIT',
    description='Key Length Value encoding and decoding',
    long_description=long_description,
    long_description_content_type='text/markdown; charset=UTF-8; variant=GFM',
    author='Arts Alliance Media',
    author_email='dev@artsalliancemedia.com',
    url='https://github.com/mjohnsullivan/python-klv',
    packages=('klv',),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
