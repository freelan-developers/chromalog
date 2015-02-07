from setuptools import (
    setup,
    find_packages,
)

setup(
    name='chromalog',
    url='http://chromalog.readthedocs.org/en/latest/index.html',
    author='Julien Kauffmann',
    author_email='julien.kauffmann@freelan.org',
    license='GPLv3',
    version=open('VERSION').read().strip(),
    description=(
        "Enhance Python with colored logging"
    ),
    long_description="""\
Default Python logging is monochromatic and boring.

Chromalog enhances it with level/based colored loggers and the ability to
highlight important elements of a given log entry.
""",
    packages=find_packages(exclude=[
        'tests',
    ]),
    install_requires=[
    ],
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
    ],
)
