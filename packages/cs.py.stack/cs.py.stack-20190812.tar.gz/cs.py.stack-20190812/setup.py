#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py.stack',
  description = 'Convenience functions for the python execution stack.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190812',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  include_package_data = True,
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description = "*Release 20190812*:\nstack_dump(): trim the last 2 frames from the listing by default (they are part of stack_dump's implementation).\n\nI find the supplied python traceback facilities quite awkward.\nThese functions provide convenient facilities.\n\n## Function `caller(frame_index=-3)`\n\nReturn the `Frame` of the caller's caller.\n\nUseful `frame_index` values:\n* `-1`: caller, this function\n* `-2`: invoker, who wants to know the caller\n* `-3`: the calling function of the invoker\n\nThe default `from_index` value is `-3`.\n\n## Class `Frame`\n\nMRO: `Frame`, `builtins.tuple`  \nA `namedtuple` for stack frame contents.\n\n## Function `frames()`\n\nReturn the current stack as a list of `Frame` objects.\n\n## Function `stack_dump(fp=None, indent=0, Fs=None, skip=None)`\n\nRecite current or supplied stack to `fp`, default `sys.stderr`.\n\nParameters:\n* `fp`: the output file object, default `sys.stderr`\n* `indent`: how many spaces to indent the stack lines, default `0`\n* `Fs`: the stack `Frame`s to write,\n  default obtained from the current stack\n* `skip`: the number of `Frame`s to trim from the end of `Fs`;\n  if `Fs` is `None` this defaults to `2` to trim the `Frame`s\n  for the `stack_dump` function and its call to `frames()`,\n  otherwise the default is `0` to use the supplied `Frame`s as is\n\n\n\n# Release Log\n\n*Release 20190812*:\nstack_dump(): trim the last 2 frames from the listing by default (they are part of stack_dump's implementation).\n\n*Release 20190101*:\n_Frame: rename .functionname to .funcname; caller: turn raw frames into Frames.\ncaller(): accept optional frame_index, default -3.\n\n*Release 20160827*:\nAdd stack_dump().\n\n*Release 20150115*:\nPyPI metadata fixups.\n\n*Release 20150111*:\nTag for initial PyPI release of cs.py.stack.",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py.stack'],
)
