# Compytition

Programming contest server in Python.

## Setup

#### Install dependencies (with `sudo` or inside of a `virtualenv`):

```bash
$ pip install -U -r requirements.txt
```

`pip` can usually be found in your distribution's `python-pip` package. If you want to use LDAP authentication (currently the only supported method), you will also need the `python-ldap` package.

#### Run the setup script

```bash
$ bumpy setup
```

#### Configure the server:

Copy `compytition/config.py.example` to `compytition/config.py` and edit it. If you have `$EDITOR` set, this will do the work for you:

```bash
$ bumpy config
```

#### Create a new contest:

```bash
$ bumpy new <name>
```

#### Add / edit questions:

Throw text files (with Markdown, if you'd like) into `contests/<name>/questions/` with **no extension**.

#### Create contest database:

```bash
$ bumpy init <name>
```

#### Run the server:

For debug or development:

***Do not use this for hosting contests! It allows execution of arbitrary Python code on the host.***

```bash
$ bumpy debug
```

For production:

```bash
$ bumpy run
```
