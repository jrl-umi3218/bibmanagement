# Bibmanagement

Quick overview
--------------
This is a small library in python, meant to manipulate programatically a bibliography, with emphasize on the output formatting.
The bibliography is read from a `.bib` file, with additional data on journal, conference or authors loaded from `.json` files. The ouput formatting can be specified by a string, and ouput to text, word or excel files are supported.

Some examples of use can be found in the 'scripts' folder, in particular in 'scripts/main.py'.

How to update bib
--------------
```bash
cd src
../scripts/gen.py <path to jrl-publi> <path to jrl-umi3218.github.com>
mv <path to jrl-publi>/tmp/*.bib <path to jrl-umi3218.github.com>/en/assets/bib
mv <path to jrl-publi>/tmp/publications.yml <path to jrl-umi3218.github.com>/_data
```
See https://github.com/jrl-umi3218/bibmanagement/issues/1#issuecomment-1237884191 for more information.
