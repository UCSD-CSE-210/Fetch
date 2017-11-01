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

Install locally to `$HOME/postgres` (tested on Xubuntu 17.04 / Zesty):
```shell
wget https://ftp.postgresql.org/pub/source/v10.0/postgresql-10.0.tar.gz
tar xf postgresql-10.0.tar.gz
cd postgresql-10.0
sudo apt-get install libreadline-dev
./configure --prefix=$HOME/postgres/ --with-python PYTHON=/usr/bin/python2.7
make -j
make install
~/postgres/bin/initdb -D ~/postgres/data/
```

To start the db server:
``` shell
~/postgres/bin/pg_ctl -D ~/postgres/data/ -l /tmp/pg-logfile start
```

To set up the database (username: fetch_db, password: fetch_db):

``` shell
> ~/postgres/bin/psql postgres

CREATE DATABASE fetch_db;
CREATE ROLE fetch_db LOGIN PASSWORD 'fetch_db';
GRANT ALL PRIVILEGES ON DATABASE fetch_db TO fetch_db;
\q

```

#### Installing PostGIS

Install the dependencies (tested on Xubuntu 17.04 / Zesty):

``` shell
sudo apt-get install libgeos-dev libxml2-dev libproj-dev libgdal-dev
```

Download and build PostGIS 2.14

``` shell
wget http://download.osgeo.org/postgis/source/postgis-2.4.1.tar.gz
cd postgis-2.4.1
PATH="$HOME/postgres/bin:$PATH" ./configure
PATH="$HOME/postgres/bin:$PATH" make
PATH="$HOME/postgres/bin:$PATH" make install
```

```shell
> ~/postgres/bin/psql fetch

CREATE EXTENSION postgis;
\q
```

