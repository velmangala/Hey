from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import *
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_completed = db.Column(db.Boolean, default=False)

    # Relationships
    support_groups = db.relationship(
        'SupportGroup', backref='users', lazy=True)
    forum_posts = db.relationship('ForumPost', backref='users', lazy=True)
    messages_sent = db.relationship(
        'Message', foreign_keys='Message.sender_id', backref='users', lazy=True)
    messages_received = db.relationship(
        'Message', foreign_keys='Message.receiver_id', backref='received_by', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def complete_profile(self):
        self.profile_completed = True
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'
    
    def load_user(user_id):
        # Implement code to load and return the user based on the user_id
        # This could involve querying your database or other user storage mechanism
        # Return the user object if found, or None if not found
        return User.query.get(user_id)

class SupportGroup(db.Model):
    __tablename__ = 'support_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creator_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    creator = db.relationship(
        'User', backref='support_groups_created', foreign_keys=[creator_id])
    members = db.relationship(
        'User', secondary='support_group_members', backref='support_groups_joined')
    forum_posts = db.relationship(
        'ForumPost', backref='support_group', lazy=True)


    def __repr__(self):
        return f'<SupportGroup {self.name}>'


class SupportGroupMember(db.Model):
    __tablename__ = 'support_group_members'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(
        'support_groups.id'), primary_key=True)


class ForumPost(db.Model):
    __tablename__ = 'forum_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    support_group_id = db.Column(db.Integer, db.ForeignKey(
        'support_groups.id'), nullable=False)

    # Relationships
    author = db.relationship('User', backref='authored_posts')
    comments = db.relationship('Comment', backref='forum_post', lazy=True)

    def __repr__(self):
        return f'<ForumPost {self.title}>'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'forum_posts.id'), nullable=False)

    # Relationships
    author = db.relationship('User', backref='comments')

    def __repr__(self):
        return f'<Comment {self.id}>'
    
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    sender = db.relationship('User', foreign_keys=[
                             sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[
                               receiver_id], backref='received_messages')

    def __repr__(self):
        return f'<Message {self.id}>'
