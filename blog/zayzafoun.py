#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3, os, datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, current_app
from contextlib import closing
from werkzeug.contrib.atom import AtomFeed
from urllib.parse  import urljoin

# Creating the application.
app = Flask(__name__)
app.config.from_object("config")

@app.context_processor
def variables_def():
  return dict(
        websiteName=app.config["WEBSITENAME"],
        websiteDesc=app.config["WEBSITEDESC"],
        websiteUrl=request.url_root[:-1],
        disqusName=app.config["DISQUSNAME"],
        currentUrl=request.path,
        )

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource(os.path.join(os.getcwd(), "schema.sql"), mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def get_pages():
  fetch_pages = g.db.execute('select * from pages order by pageid')
  pages = [dict(pageid=y[0], pageurl=y[1], pagetitle=y[2]) for y in fetch_pages.fetchall()]
  return pages

def get_posts():
  posts = ""
  fetch_posts = g.db.execute('select * from posts order by postid desc')
  posts = [dict(postid=x[0], posttitle=x[1], posturl=x[2], postcontent=x[3], postauthor=x[4], postdate=x[5]) for x in fetch_posts.fetchall()]
  return posts

def single_post(posturl):
  showingpost = g.db.execute('select * from posts where posturl = ?', (posturl,))
  for x in showingpost.fetchall():
    postid, posttitle, posturl, postcontent, postauthor, postdate = x[0], x[1], x[2], x[3], x[4], x[5]
  post = [postid, posttitle, posturl, postcontent, postauthor, postdate]
  return post

def editpost(posturl):
  if session.get('logged_in'):
    getPost = g.db.execute('select * from posts where posturl = ?', (posturl,))
    for n in getPost.fetchall():
      posttitle, posturl, postcontent = n[1], n[2], n[3]
    post = [posttitle, posturl, postcontent]
    return post
  else:
    abort(404)

def single_page(pageurl):
  showingpage = g.db.execute('select * from pages where pageurl= ?', (pageurl,))
  for x in showingpage.fetchall():
    pageid, pageurl, pagetitle, pagecontent, pageauthor, pagedate = x[0], x[1], x[2], x[3], x[4], x[5]
  page = [pageid, pageurl, pagetitle, pagecontent, pageauthor, pagedate]
  return page

def editpage(pageurl):
  if session.get('logged_in'):
    getPage = g.db.execute('select * from pages where pageurl = ?', (pageurl,))
    for n in getPage.fetchall():
      pagetitle, pageurl, pagecontent, = n[1], n[2], n[3]
    page = [pageurl, pagetitle, pagecontent]
    return page
  else:
    abort(404)

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.route('/')
def show_index():
  return render_template('index.html', posts=get_posts(), pages=get_pages())

@app.route('/post/<posturl>')
def show_post(posturl):
  return render_template('post.html', post=single_post(posturl), posts=get_posts(), pages=get_pages())

@app.route('/post/<posturl>/edit')
def postedit(posturl):
  if session.get('logged_in'):
    return render_template('edit.html', post = editpost(posturl), contentType = "post", pages=get_pages())
  else:
    abort(404)

@app.route('/post/<posturl>/delete')
def postdelete(posturl):
  if session.get('logged_in'):
    g.db.execute('delete from posts where posturl = ?', (posturl,))
    g.db.commit()
    return render_template('index.html', posts=get_posts(), pages=get_pages())
  else:
    abort(404)

@app.route('/page/<pageurl>')
def show_page(pageurl):
  return render_template('page.html', page=single_page(pageurl), pages=get_pages())

@app.route('/page/<pageurl>/edit')
def pageedit(pageurl):
  if session.get('logged_in'):
    return render_template('edit.html', post = editpage(pageurl), contentType = "page", pages=get_pages())
  else:
    abort(404)

@app.route('/page/<pageurl>/delete')
def pagedelete(pageurl):
  if session.get('logged_in'):
      g.db.execute('delete from pages where pageurl = ?', (pageurl,))
      g.db.commit()
      return render_template('index.html', posts=get_posts(), pages=get_pages())
  else:
    abort(404)

@app.route('/archive')
def archive():
      return render_template('archive.html', posts=get_posts(), pages=get_pages())

@app.route('/publish', methods=['GET', 'POST'])
def publish():
  if session.get('logged_in'):
    if request.method == 'POST':
      if request.form["contenttype"] == "post":
        g.db.execute('insert into posts (posttitle, posturl, postcontent, postauthor) values (?, ?, ?, ?)',
                     (request.form['title'], request.form['url'], request.form['content'], session['username']))
        g.db.commit()
        return redirect(request.url_root)
      else:
        g.db.execute('insert into pages (pagetitle, pageurl, pagecontent, pageauthor) values (?, ?, ?, ?)',
                     (request.form['title'], request.form['url'], request.form['content'], session['username']))
        g.db.commit()
        return redirect(request.url_root)
    elif request.method == 'GET':
      return render_template('new.html', pages=get_pages())
  else:
    return abort(404)

def make_external(url):
  return urljoin(request.url_root, url)


@app.route('/posts.atom')
def recent_feed():
  feed = AtomFeed('Recent Articles',
                  feed_url=request.url, url=request.url_root)
  articles = get_posts()[:5]
  for y in range(len(articles)):
      feed.add(articles[y]['posttitle'], articles[y]['postcontent'],
               content_type='html',
               url=make_external(articles[y]['posturl']),
               updated=datetime.datetime.strptime(articles[y]['postdate'], '%Y-%m-%d %H:%M:%S'))
  return feed.get_response()

@app.route('/publishedit', methods=['POST'])
def doEdit():
  if session.get('logged_in'):
    if request.method == 'POST':
      if request.form["contenttype"] == "post":
        g.db.execute('UPDATE posts SET posttitle = ?, postcontent = ? WHERE posturl = ?', (request.form['title'], request.form['content'], request.form['url']))
        g.db.commit()
        return redirect(request.url_root)
      else:
        g.db.execute('UPDATE pages SET pagetitle = ?, pagecontent = ? WHERE pageurl = ?', (request.form['title'], request.form['content'], request.form['url']))
        g.db.commit()
        return redirect(request.url_root)
    else:
        abort(404)
  else:
    abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if session.get('logged_in'):
    return redirect(request.url_root)
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      session['username'] = app.config['USERNAME']
      return redirect(request.url_root)
  return render_template('login.html', pages=get_pages())


@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  return redirect(request.url_root)

if __name__ == "__main__":
  init_db()
  app.run(host='0.0.0.0', port=5000)
