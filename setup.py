from setuptools import setup, find_packages
from pathlib import Path
DESCRIPTION = 'Simplified Earth magnetosheath model'

this_directory = Path(__file__).parent
LONG_DESCRIPTION =  (this_directory / "README.md").read_text()

setup(
    name='Mshpy',
    version='0.1.3',
    packages=find_packages(),
    package_data={'Mshpy': ['data/**/*']},
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    install_requires=[
        'sympy'
    ],
    include_package_data=True,
)