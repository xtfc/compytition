# Compytition

Programming contest server in Python.

## Setup

Initialize submodules:

```bash
$ git submodule init
$ git submodule update
```

Install dependencies (with `sudo` or inside of a `virtualenv`):

```bash
$ pip install -U -r requirements.txt
```

Configure the server:

```bash
$ $EDITOR compytition/config.py
```

Write some questions:

```bash
$ mkdir -p questions
$ echo "How write question?" > questions/q1
...
```

Initialize database:

```bash
$ python
>>> from compytition import db
>>> db.init()
$
```

Run the dev server:

```bash
$ python -m compytition
```
