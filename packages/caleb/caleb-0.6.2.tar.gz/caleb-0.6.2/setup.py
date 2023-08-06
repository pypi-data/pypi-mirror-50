# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['caleb']

package_data = \
{'': ['*']}

install_requires = \
['crossref-commons>=0.0.6,<0.0.7',
 'mypy>=0.720.0,<0.721.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['caleb = caleb.cmdline:launch']}

setup_kwargs = {
    'name': 'caleb',
    'version': '0.6.2',
    'description': 'A tool to automatically retrieve bibtex entries',
    'long_description': "# caleb\n\n[![PyPI version](https://badge.fury.io/py/caleb.svg)](https://badge.fury.io/py/caleb)\n[![Coverage Status](https://coveralls.io/repos/github/kevinywlui/caleb/badge.svg?branch=master)](https://coveralls.io/github/kevinywlui/caleb?branch=master)\n[![Build Status](https://travis-ci.org/kevinywlui/caleb.svg?branch=master)](https://travis-ci.org/kevinywlui/caleb)\n\n**caleb** is a tool to automatically fill in your Latex citations.\n\n## Usage examples\n\nSee the `examples` directory along with the `an_example.tex` file. The\nfollowing examples occur in the `examples` directory.\n\n* First run `pdflatex an_example.tex ` to generate `an_example.aux`. `caleb`\n  will now parse `an_example.aux` to generate the appropriate bibliography\n  file.\n```\ncaleb an_example\n```\n\n* The first important commandline option is `--take-first`. When making a\n  query, it is possible that there are multiple result. By default, `caleb`\n  will take no action here. However, if the `--take-first` flag is passed,\n  `caleb` will take the first entry.\n```\ncaleb --take-first an_example\n```\n\n* The next important commandline option is `--method`. By default, `caleb` uses\n  `crossref.org`. However, we can also tell `caleb` to use\n  <https://mathscinet.ams.org/mrlookup>.\n```\ncaleb --method ams\n```\n\n## Workflow integration\n\n### latexmk\n\n* The best way is probably to integrate into `latexmk`. The `-pdflatex` flag\n  allows us to run `caleb` after each `pdflatex` call.\n```\nlatexmk -pdf -pdflatex='pdflatex %O %S; caleb -t -m ams %B' an_example\n```\n\n* We can set the `-pdflatex` flag in a `.latexmkrc` file. This can either go in\n  the your tex project folder or in the home directory. So in the `.latexmkrc`\n  file, include the following line (see examples directory for an example):\n```\n$pdflatex='pdflatex %O %S; caleb %B'\n```\n\n### Barebones\n\n* The barebone approach is to run `caleb` before running bibtex.\n```\npdflatex an_example\ncaleb an_example\nbibtex an_example\npdflatex an_example\npdflatex an_example\n```\n\n### cocalc\n\n<http://cocalc.com> contains a collaborative latex editor that allows you to use a\ncustom build command. We can use `caleb` by changing it to\n```\nlatexmk -pdf -pdflatex='pdflatex %O %S; caleb -t -m ams %B' -f -g -bibtex -synctex=1 -interaction=nonstopmode an_example.tex\n```\n\n\n## Help\n\n`caleb` comes with some command line arguments.\n```\n$ caleb --help\nusage: caleb [-h] [-t] [-v] [--version] [-m {crossref,ams}] [input_name]\n\npositional arguments:\n  input_name\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -t, --take-first      Take first result if multiple results\n  -v, --verbose         Increase verbosity of output\n  --version             Outputs the version\n  -m {crossref,ams}, --method {crossref,ams}\n                        Specify a method for retrieving citations\n```\n\n## Installation\n\n### Dependencies\n\n* [crossref_commons_py](https://gitlab.com/crossref/crossref_commons_py)\n* [requests](https://3.python-requests.org/)\n* `python3`\n\n### Testing and Development Dependencies\n\n* [python-coveralls](https://github.com/z4r/python-coveralls)\n* [pytest](https://pytest.org/en/latest/)\n* [pytest-cov](https://github.com/pytest-dev/pytest-cov)\n* [black](https://github.com/psf/black)\n\n### `pip`\n\n```\npip3 install caleb --user\n```\n\n### `setup.py`\n\n```\npython setup.py install --user\n```\n\n\n## Goal of project\n\n* [ ] Reach feature parity with IRL [Caleb](https://sites.math.washington.edu/~geigerc/)\n\n## Homepage\n\n* https://github.com/kevinywlui/caleb\n",
    'author': 'kevin lui',
    'author_email': 'kevinywlui@gmail.com',
    'url': 'https://github.com/kevinywlui/caleb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
