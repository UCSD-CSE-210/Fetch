Fetch Flask App
==============

#### Getting Started
1. Set up a virtual environment. If virtualenv is not installed, follow the instructions at https://virtualenvwrapper.readthedocs.io/en/latest/
    - `mkvirtualenv fetch`
2. Install all of the dependencies
    - `pip install -r requirements.txt`
3. Create the database
    - `python create_db.py`
4. Start the server
    - `FLASK_APP=fetch.py flask run`

#### Installing PostgreSQL locally

```
./configure --prefix=$HOME/postgres/ --with-python PYTHON=/usr/bin/python2.7
make -j
make install
...
~/postgres/bin/initdb -D ~/postgres/data/
```
