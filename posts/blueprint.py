from flask import Blueprint
from flask import render_template

from models import Post, Tag
from app import db

from flask import request

from .forms import PostForm

from flask import redirect, url_for

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Error')
        return redirect(url_for('posts.index'))
    else:
        form = PostForm()
        return render_template('posts/create_post.html', form=form)


@posts.route('/')
def index():
    query = request.args.get('query')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.body.contains(query)).all()
    else:
        posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    return render_template('posts/tag_detail.html', tag=tag)
