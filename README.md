# Compytition

Programming contest server in Python.

## Setup

#### Initialize submodules:

```bash
$ git submodule init
$ git submodule update
```

#### Install dependencies (with `sudo` or inside of a `virtualenv`):

```bash
$ pip install -U -r requirements.txt
```

#### Configure the server:

Copy `compytition/config.py.example` to `compytition/config.py` and edit it. If you have `$EDITOR` set, this will do the work for you:

```bash
$ bumpy config
```

#### Create a new contest:

```bash
$ bumpy new example
```

#### Add / edit questions:

Throw text files (with Markdown, if you'd like) into `contests/example/questions/` with **no extension**.

#### Create contest database:

```bash
$ bumpy init example
```

#### Run the server:

```bash
$ bumpy run # pseudo-production server
$ bumpy debug # development server
```
