from flask import Flask, redirect, url_for, \
				  request, render_template, json
from pymongo import MongoClient
import pymongo
import os
import socket
from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient('mongodb://backend:27017/dockerdemo')
db = client.blogpostDB

app = Flask(__name__)

@app.route("/")
def landing_page():
    posts = get_all_posts()
    
    return render_template('blog.html', posts=json.loads(posts))


@app.route('/add_post', methods=['POST'])
def add_post():

    new()
    return redirect(url_for('landing_page'))

@app.route('/edit_post/<id>', methods=['POST'])
def edit_post(id):

    update(id)
    return redirect(url_for('landing_page'))

@app.route('/delete_post/<id>')
def remove_one(id):
    
    delete(id)
    return redirect(url_for('landing_page'))

@app.route('/remove_all')
def remove_all():
    db.blogpostDB.delete_many({})

    return redirect(url_for('landing_page'))




## Services

@app.route("/posts", methods=['GET'])
def get_all_posts():
    
    _posts = db.blogpostDB.find()
    print 'count'
    print _posts.count()
    posts = [post for post in _posts]
    return JSONEncoder().encode(posts)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }
    db.blogpostDB.insert_one(item_doc)

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    return JSONEncoder().encode(posts[-1])


### Insert function here ###

@app.route('/update/<id>', methods=['POST'])
def update(id):
        
    db.blogpostDB.update_one(
            {
                '_id': ObjectId(id)
            }, 
            {
                '$set': {
                    'title': request.form['title'],
                    'post': request.form['post']
                }
            }, upsert=False)

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    return JSONEncoder().encode(posts[-1])

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
        
    db.blogpostDB.delete_one({'_id': ObjectId(id)})

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    if len(posts) > 0:
        return JSONEncoder().encode(posts[-1])
    else:
        return []

############################



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
