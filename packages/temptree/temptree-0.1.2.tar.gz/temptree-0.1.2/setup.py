# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['temptree']
setup_kwargs = {
    'name': 'temptree',
    'version': '0.1.2',
    'description': 'Generates temporary files and directories from a tree',
    'long_description': 'temptree\n========\nGenerates temporary files and directories from a tree.\n\nThe provided `TemporaryTree` class allows to create complete files hierarchies under a\nroot `tempfile.TemporaryDirectory`.\n\nIt is well suited for usage within *doctests* :\n\n    >>> from temptree import TemporaryTree\n    >>> with TemporaryTree({\n    ...     "foo.py": None,\n    ...     "bar": {\n    ...         "bar.py": None,\n    ...         "baz.py": None,\n    ...     }\n    ... }) as root:\n    ...     (root / "foo.py").exists()\n    ...     (root / "bar").is_dir()\n    ...     (root / "bar" / "bar.py").is_file()\n    ...\n    True\n    True\n    True\n\nInstallation\n------------\n\nAdd `temptree` to your project dependencies:\n\n    poetry add temptree\n\nIf you just need it within your *doctests*, add it as a development dependency:\n\n    poetry add --dev temptree\n\nDocumentation\n-------------\n\n[The complete documentation][documentation] is available from Github Pages.\n\nContributing\n------------\n\nThis project is hosted on [Github][repository].\n\nIf you\'re facing an issue using `temptree`, please look at\n[the existing tickets][issues]. Then you may open a new one.\n\nYou may also make a [push request][pull-requests] to help improve it.\n\nLicense\n-------\n\n`temptree` is licensed under the [GNU GPL 3][GPL] or later.\n\n[documentation]: https://neimad.github.io/temptree/\n[repository]: https://github.com/neimad/temptree\n[issues]: https://github.com/neimad/temptree/issues\n[pull-requests]: https://github.com/neimad/temptree/pulls\n[GPL]: https://www.gnu.org/licenses/gpl.html',
    'author': 'Damien Flament',
    'author_email': 'damien.flament@gmx.com',
    'url': 'https://github.com/neimad/temptree',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
