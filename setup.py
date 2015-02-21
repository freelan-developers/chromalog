from setuptools import (
    setup,
    find_packages,
)

setup(
    name='chromalog',
    url='http://chromalog.readthedocs.org/en/latest/index.html',
    author='Julien Kauffmann',
    author_email='julien.kauffmann@freelan.org',
    maintainer='Julien Kauffmann',
    maintainer_email='julien.kauffmann@freelan.org',
    license='MIT',
    version=open('VERSION').read().strip(),
    description=(
        "A non-intrusive way to use colors in your logs and generic output."
    ),
    long_description="""\
Chromalog integrates seemlessly in any Python project and allows the use of
colors in log messages and generic output easily. It is based on colorama and
so works on both Windows and *NIX platforms. Chromalog is able to detect
without any configuration if the associated output stream has color
capabilities and can fall back to the default monochromatic logging.

Chromalog also offer helpers to easily highlight some important parts of a log
message.
""",
    packages=find_packages(exclude=[
        'tests',
        'scripts',
    ]),
    install_requires=[
        'colorama>=0.3.3',
        'future>=0.14.3',
        'six>=1.9.0',
    ],
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
    ],
)
