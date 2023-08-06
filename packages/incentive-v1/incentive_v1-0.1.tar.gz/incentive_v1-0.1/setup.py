import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='incentive_v1',
    version='0.1',
    packages=['incentive_v1'],
    description='A line of description',
    long_description=README,
    author='rajesh',
    author_email='rajesh@peerbits.com',
    url='https://github.com/yourname/django-myapp/',
    license='MIT',
    install_requires=[
        'Django>=1.6,<2.2',
    ]
)