from setuptools import setup

import oraide

setup(
    name='oraide',
    version=oraide.__version__,
    author='Daniel D. Beck',
    author_email='me@danieldbeck.com',
    description=('A library to help presenters demonstrate terminal sessions '
                 'hands-free.'),
    url='https://github.com/ddbeck/oraide',
    license='BSD',
    long_description=open('README.rst').read(),
    keywords=['tmux', 'presentation', 'demonstration'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
    packages=['oraide'],
    test_suite='oraide.tests',
    zip_safe=True,
)
