from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import *
from datetime import datetime

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
        'SupportGroup', backref='creator', lazy=True)
    forum_posts = db.relationship('ForumPost', backref='author', lazy=True)
    messages_sent = db.relationship(
        'Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    messages_received = db.relationship(
        'Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def complete_profile(self):
        self.profile_completed = True
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'


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
    author = db.relationship('User', backref='forum_posts')
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
