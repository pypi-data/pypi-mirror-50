# benc: Python3 Bencode (en|de)coder

![build-status](https://circleci.com/gh/notpeter/benc.svg?style=shield&circle-token=:circle-token)
![pypi-version](https://img.shields.io/pypi/v/benc.svg)

Bencoder in 100 lines of modern Python (MIT License)

## Install

```
pip3 install -U benc
```

## Simple Usage

```python
import benc

benc.encode(43)
# b'i43e'

benc.encode({b'env':b'python', b'lang': [b'en', b'es']})
# b'd3:env6:python4:langl2:en2:esee'

benc.decode(b'd8:language6:pythone')
# {b'language': b'python'}

```

## Torrent example
```python
import datetime, hashlib, benc

with open("ubuntu-18.04.2-live-server-amd64.iso.torrent", 'rb') as f:
    torrent = benc.decode(f)

print(torrent[b'info'][b'name'])
# b'ubuntu-18.04.2-live-server-amd64.iso'

print(datetime.datetime.utcfromtimestamp(torrent[b'creation date']).isoformat())
# '2019-02-14T22:53:17'

hashlib.sha1(benc.encode(torrent[b'info'])).hexdigest()
# '842783e3005495d5d1637f5364b59343c7844707'
```

## Bencode Background

[Bencode](https://en.wikipedia.org/wiki/Bencode) is a serialization/encoding format
used by BitTorrent for transmitting loosely structured data.  Unlike JSON or msgpack
it is notable because input/output are consistent between implementions for a given
data structure: there is a [bijection](https://en.wikipedia.org/wiki/Bijection)
between the two, resulting in one (and only one) (de)serialization for any given input.

## Types

Bencode supports four data types:

* int: `-42` -> `i-42e`
* str: `'spam'` -> `4:spam`
* list: `[b'XYZ', 4321]` -> `l3:XYZi4321ee`
* dict: `{b'XYZ': 4321}'` -> `d3:XYZi4321ee`

Unsupported types:
  * null
  * float

Gotchas:
* No floats
* Strings are UTF-8 encoded
* Dictionary keys are bytes not strings. This is required because keys may
contain arbitrary bytes that may be invalid UTF-8.

## Why another bencode library?

benc.py is a MIT licensed, single file pure-python re-implementation of
Bencode for modern Python with no external requirements.  I've taken a
TDD approach starting with a set of tests cases from other existing bencode
implementations and worked backawards from there.

It requires Python >= 3.6 because it uses the following features:
* [PEP 484](https://www.python.org/dev/peps/pep-0484/) - Type Hints (Python 3.6)
* [PEP 498](https://www.python.org/dev/peps/pep-0498/) - F-Strings (Python 3.6)
* [PEP 460](https://www.python.org/dev/peps/pep-0460/) - Bytearray string interp (Python 3.5)

There are many alternative implementations of Bencode but many have license
concerns, Python3 and UTF-8 issues and haven't been updated in ages.  Very few
have tests.

The original bencode.py from the Mainline BitTorrent client (written by @ppetru)
is not Python3 compatible and has not been significantly updated it's initial
release in 2004  It has had multiple licenses, none of which are particularly friendly:

* [BitTorrent Open Source License](http://www.bittorrent.com/license/) (original release)
* [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
(see [BitTorrent-4.0.0-GPL.tar.gz](http://web.archive.org/web/20110814224849/http://download.bittorrent.com/dl/BitTorrent-4.0.0-GPL.tar.gz))
* [Python Software Foundation License Version 2.3](https://www.python.org/download/releases/2.3/license/)
(see [BitTorrent-5.3-GPL.tar.gz](http://web.archive.org/web/20110814224849/http://download.bittorrent.com/dl/BitTorrent-5.3-GPL.tar.gz))

## Comparison

Last updated: 2019-07-31

| pypi package | license | updated | source | python2 | python3 | notes |
| ------------ | ------- | ------- | ------ | ------- | ------- | ----- |
| [bencode](https://pypi.org/project/bencode/) | [BitTorrent Open Source 1.1](https://github.com/bittorrent/bencode/blob/master/LICENSE.txt) | 2010-12-30 | [bittorrent/bencode](https://github.com/bittorrent/bencode) | yes | no | Repackaged from BitTorrent 5.0.8 |
| [bencode3](https://pypi.org/project/bencode3/) | MIT | 2018-07-17 | [bitbucket.org/tinyproxy/bencode3](https://bitbucket.org/tinyproxy/bencode3/src/master/) | no | yes | Port of official Bencode to Python3. MIT license questionable.
| [bencoder](https://pypi.org/project/bencoder/) | unknown | 2016-09-07 | [utdemir/bencoder](https://github.com/utdemir/bencoder) | no | yes |
| [bcode] | MIT | []
