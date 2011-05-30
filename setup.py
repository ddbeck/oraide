from setuptools import setup

reqs = []
try:
    import argparse
except ImportError:
    reqs = ['argparse']

setup(
    name='oraide',
    version='0.1',
    license='BSD',
    url='http://github.com/ddbeck/oraide',
    author='Daniel D. Beck',
    author_email='me@danieldbeck.com',
    description='A tool to spare presenters the risky proposition of '
                'entering terminal commands and giving a presentation at '
                'the same time.',
    long_description=open('README').read(),
    packages=['oraide'],
    scripts=['bin/oraide'],
    install_requires=reqs,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
