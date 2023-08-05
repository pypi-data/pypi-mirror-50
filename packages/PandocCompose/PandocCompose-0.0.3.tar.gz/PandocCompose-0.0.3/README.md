# Usage

`pandoc-compose` lets you manage your documentation base by automating
conversion of mutiple markdown or other formatted text files using Pandoc.

Pandoc should be already installed on you computer.

## How does it work?

Just like `docker-compose`, when executed, `pandoc-compose` will search for a
`pandoc-compose.yml` file either in current working directory or in a sepcified
destination (see [Synpsis](#synpsis)) and extract configuration from it to
automate the conversion of you document base from any input format to any output
format supported by Pandoc.

See [the documentation](./DOCUMENTATION.md) for more informations on how to use
it.

# TODO

* auto-install pandoc
* option to specify the metadata file
* pass metadata variables directly from command line
* extend `pandoc-compose.yml` :
  * une detection of file (for instance using regexes)
  * change format
  * add of remove [extensions](https://pandoc.org/MANUAL.html#extensions)
