from setuptools import setup, find_packages
from reciprocalblast import __version__

setup(
    name='reciprocalblast',
    version=__version__,
    author='Kent Kawashima',
    author_email='kentkawashima@gmail.com',
    description='Perform reciprocal blastn analysis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=['blast', 'search', 'sequence', 'dna', 'bioinformatics'],
    packages=find_packages(),
)
