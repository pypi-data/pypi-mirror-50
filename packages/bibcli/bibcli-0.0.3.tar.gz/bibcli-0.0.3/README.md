# bib – command-line bibliography manager

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## What?

bib is a _command-line bibliography manager_. That means it **manages
bibliograpies**. From the **command-line**.

What does that mean? Basically, bib stores all of your references in a
[BibTeX](https://en.wikipedia.org/wiki/BibTeX) file, along with notes and PDFs
that might be associated with them. To make that useful, it provides a
command-line interface for `add`ing new items, `import`ing PDFs, creating
`note`s, `export`ing sub-bibliographies, `list`ing the items according to a
query, _etc_.

## Why?

I've used Zotero for some time. It's nice, it does everything that I need it to.
The problem is… it does to much. It is, in the language of the cool-hackerboys,
“bloated”. Aside from that, I believe (as it has been said elsewhere), that
_plaintext is the only truly portable format_. Finally, I like to pretend I'm
smarter than I am, so I use the command line.

To my surprise, there wasn't any command line bibliography manager. So I build
one.

I'm not saying it's good (although I'd like it to be), nor that you'll like it
(I hope you do try it). But I like it, and would love contributions. Anyway,
enough pointless talking.

## Installation

bib is available at the Python Package Index. That means, if you have Python and
`pip` installed, it should be enough to

```bash
$ pip install bib
```

If you want to install from source, clone the repository and use the `setup.py`
as you would with any other Python package.

## License

bib is free software. The details can be found in the `LICENSE.txt` file, or
otherwise reading about the GNU Public License v3+.

## Contributing

This is currently a small, one-person project. Also, I don't have much
experience in writing distributed code, so if you have any suggestions, they are
highly appreciated. Otherwise, I can't really direct contributions because I
haven't worked in many-people code bases. Any input on _that_ would also be
helpful.

