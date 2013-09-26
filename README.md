# Compytition

Programming contest server in Python.

## Setup

Initialize submodules:

```bash
$ git submodule init
$ git submodule update
```

Install dependencies:

```bash
$ pip install -U -r requirements.txt
```

Configure the server:

```bash
$ $EDITOR compytition/config.py
```

Initialize database:

```bash
$ python
>>> from compytition import db
>>> db.init()
$
```

Write some questions:

```bash
$ mkdir -p questions
$ echo "How write question?" > questions/q1
...
```

Run the dev server:

```bash
$ PYTHONPATH=. python -m compytition
```
