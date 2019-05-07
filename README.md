# Warbler
A Twitter Clone <br/>
See it: https://warbler-less.herokuapp.com/

##Technologies
* Flask 1.0.2
* Flask-Bcrypt 0.7.1
* Flask-DebugToolbar 0.10.1
* Flask-SQLAlchemy 2.3.2
* Flask-WTF 0.14.2
* Jinja2 2.10
* psycopg2-binary 2.7.5
* bootstrap

## To run the app on local

Set up folder:
```
 git clone git@github.com:ivyc81/Warbler.git
 cd Warbler
 python3 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
```

Set up database:
```
createdb warbler
python seed.py
```

Start app:
```
 flask run # Open browser to localhost:5000 and try the app out!
```

## To run tests
```
createdb warbler-test
python -m unittest test_file_name
```
