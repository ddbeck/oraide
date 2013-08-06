from setuptools import setup

setup(
    name='oraide',
    version='0.3.0',
    author='Daniel D. Beck',
    author_email='me@danieldbeck.com',
    description=('A library to help presenters demonstrate terminal sessions '
                 'hands-free.'),
    url='https://github.com/ddbeck/oraide',
    license='BSD',
    long_description=open('README.rst').read(),
    packages=['oraide'],
    test_suite='oraide.tests',
)
