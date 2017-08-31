from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


#model class attributes????
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(400))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog')
def blog():
    if request.args.get('id'):
        blog_id = int(request.args.get('id'))
        this_blog = Blog.query.get( blog_id )

        if this_blog:
            return render_template('entry.html', page_header=this_blog.title, blog=this_blog)
        else:
            Blog_not_found = "No entries as of yet"
            return render_template('entry.html',Blog_not_found=Blog_not_found, page_header="Blog Not Found")

    blog_id = request.args.get('id')

    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog.html', posts=posts, title='Build-a-blog')
 
    
@app.route('/')
def index():
    return redirect('/blog') #Lets go straight to BLOG

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title_error = ''
    body_error = ''

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-entry']
        if len(blog_title) < 10:
            title_error = "Your tittle must be at least 10 characters long kid."
        if not blog_title:
            title_error = "Can't leave blank!"
        if len(blog_body) < 20:  
            body_error = "You need some more content there bud."
        if not blog_body:
            body_error = "Enter a blog entry son."

        if not body_error and not title_error:
            new_entry = Blog(blog_title, blog_body)     
            db.session.add(new_entry)
            db.session.commit() 

            return redirect('/blog?id='+str(new_entry.id)) 
        else:
            return render_template('newpost.html', title='New Entry', title_error=title_error, body_error=body_error, 
                blog_title=blog_title, blog_body=blog_body)

    return render_template('newpost.html', title='New Entry')
    
def reboot(self):
    def decorator(f):
        import re
        import commands
        s = commands.getoutput('lsof -i :5000')
        try:
            p_id = re.findall('.*?Python\s+[0-9]{4,7}', s)[0].split(' ')[-1]
        except IndexError:
            p_id = None
        p_id = int(p_id) if p_id else None
        if p_id:
            commands.getoutput('kill -9 {}'.format(p_id))
        return f
    return decorator

if  __name__ == "__main__":
    app.run()