"""Command to show the raw bibtex of a given paper

Can show the bibtex of a paper present in the repository:
```
pubs bibtex Loeb_2012
```
Or downloaded, using a DOI, ISBN or arXiv reference, using the same syntax
as the `add` command.
```
pubs bibtex -X 1803.10122
```
"""

import argparse
from ..uis import get_ui
from .. import p3
from .. import bibstruct
from .. import content
from .. import repo
from .. import paper
from .. import templates
from .. import apis
from .. import pretty
from .. import utils
from .. import endecoder
from ..command_utils import add_doc_copy_arguments
from ..completion import CommaSeparatedTagsCompletion

from .add_cmd import ValidateDOI, bibentry_from_api


def parser(subparsers, conf):
    parser = subparsers.add_parser('bibtex', help='show the bibtex of a reference')
    parser.add_argument('citekey', nargs='?', default=None,
                        help='citekey, for a paper in the repository')
    id_arg = parser.add_mutually_exclusive_group()
    id_arg.add_argument('-D', '--doi', help='doi number to retrieve the bibtex entry', default=None, action=ValidateDOI)
    id_arg.add_argument('-I', '--isbn', help='isbn number to retrieve the bibtex entry', default=None)
    id_arg.add_argument('-X', '--arxiv', help='arXiv ID to retrieve the bibtex entry', default=None)
    return parser



def command(conf, args):
    """
    """

    ui = get_ui()
    citekey = args.citekey

    rp = repo.Repository(conf)

    if citekey is None:
        bibentry = bibentry_from_api(args, ui, raw=True)
        if bibentry is not None:
            print(bibentry)
