[![Build Status](https://travis-ci.org/freelan-developers/chromalog.svg)](https://travis-ci.org/freelan-developers/chromalog)
[![Documentation Status](https://readthedocs.org/projects/chromalog/badge/?version=latest)](https://readthedocs.org/projects/chromalog/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/freelan-developers/chromalog/badge.svg?branch=master)](https://coveralls.io/r/freelan-developers/chromalog?branch=master)
[![Development Status](https://pypip.in/status/chromalog/badge.svg)](https://pypi.python.org/pypi/chromalog)
[![Wheel Status](https://pypip.in/wheel/chromalog/badge.png?branch=master)](https://pypi.python.org/pypi/chromalog)
[![License](https://img.shields.io/pypi/l/chromalog.svg)](http://opensource.org/licenses/MIT)
[![GitHub Tag](https://img.shields.io/github/tag/freelan-developers/chromalog.svg)](https://github.com/freelan-developers/chromalog)
[![Latest Release](https://img.shields.io/pypi/v/chromalog.svg)](https://pypi.python.org/pypi/chromalog)

# Chromalog

**Chromalog** is a Python library that eases the use of colors in Python logging.

It integrates seamlessly into any Python 2 or Python 3 project. Based on colorama, it works on both Windows and *NIX platforms.

**Chromalog** can detect whether the associated output stream is color-capable and even has a fallback mechanism: if color is not supported, your log will look no worse than it was before you colorized it.

Using **Chromalog**, getting a logging-system that looks like this is a breeze:

![home-sample](doc/source/_static/home-sample.png)

Its use is simple and straightforward:

    from chromalog.mark.helpers.simple import important

    logger.info("Connected as %s for 2 hours.", important(username))

Ready to add some colors in your life ? Check out [Chromalog’s documentation](http://chromalog.readthedocs.org/en/latest/index.html) !
