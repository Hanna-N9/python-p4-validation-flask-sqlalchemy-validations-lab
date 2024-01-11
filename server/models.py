from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# Add validators 
    
    # All authors have a name.
    # No two authors have the same name.
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required.")
        author = db.session.query(Author.id).filter_by(name = name).first() #Check if an author with same name already exists
        if author is not None:
            raise ValueError("This name already exists.")
        return name

    # Author phone numbers are exactly ten digits.
    @validates('phone_number')
    def validate_phone_number(self, key, pn):
        if len(pn) != 10 or not pn.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        return pn
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
       
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# Add validators  
    
    # Post content is at least 250 characters long.
    @validates('content')
    def validate_content(self, key, content):
       if len(content) < 250:
           raise ValueError("Content must be at least 250 characters.")
       return content
   
    # Post summary is a maximum of 250 characters.
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
           raise ValueError("Summary must be less than 250 characters.")
        return summary
    
    # Post category is either Fiction or Non-Fiction.
    @validates('category') 
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category
    
    # Post title is sufficiently clickbait-y and must contain one of the following: "Won't Believe", "Secret", "Top", "Guess"
    @validates('title')
    def validate_title(self, key, title):
      clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
      if not title:
            raise ValueError("Title is required.")
      if not any(term in title for term in clickbait):
          raise ValueError("Title must contain one of the following: Won't Believe, Secret, Top, Guess.")
      return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
