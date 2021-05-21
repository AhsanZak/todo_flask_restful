# REST API With Flask & SQL Alchemy

> Todo API using Python Flask, SQL Alchemy and Marshmallow


# Create DB
$ python
>> from todo import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python todo.py
```

## Endpoints

* GET     /todos
* GET     /todo/:id
* POST    /todos
* PUT     /todo/:id
* DELETE  /todo/:id