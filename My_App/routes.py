from flask_login import current_user
from crypt import methods
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_jwt import jwt_required
from forms import *
from models import *
from utils import *




app_routes = Blueprint('app_routes', __name__)
api_routes = Blueprint('api_routes', __name__)

api_routes.route('/api/register', methods=['POST'])
@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app_routes.route('/api/login', methods=['POST'])
@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "success"

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


# Logout route
@api_routes.route('/api/logout')
@app_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('app_route.index'))

@api_routes.route('/api/index')
@app_routes.route('/index')
def index():
    return 'Index Page'

@api_routes.route('/api/profile', methods=['GET', 'POST'])
@app_routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@api_routes.route('/api/edit_profile', methods=['GET', 'POST'])
@app_routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    data = request.get_json()
    # Retrieve the necessary data from the request JSON
    name = data.get('name')
    email = data.get('email')

    # Update the user's profile information
    current_user.name = name
    current_user.email = email

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response indicating success
    return jsonify({'message': 'Profile updated successfully'})


@api_routes.route('/api/complete_profile', methods=['GET', 'POST'])
@app_routes.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Update the user's profile information in the database
        current_user.name = form.name.data
        current_user.age = form.age.data
        # Add more fields as needed
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    return render_template('complete_profile.html', form=form)

@api_routes.route('/api/dashboard')
@app_routes.route('/dashboard')
@login_required  # Use the @login_required decorator to protect the route
def dashboard():
    # Route accessible only for authenticated users
    pass


@api_routes.route('/api/admin', methods=['GET', 'POST'])
@app_routes.route('/admin')
# Use the @roles_required decorator to check for specific roles
@roles_required('admin')
def admin_panel():
    # Route accessible only for users with 'admin' role
    pass


@api_routes.route('/support-group/create', methods=['GET', 'POST'])
@app_routes.route('/support-group/create', methods=['GET', 'POST'])
def create_support_group():
    form = SupportGroupForm()

    if form.validate_on_submit():
        # Create a new support group object using the form data
        support_group = SupportGroup(
            title=form.title.data,
            description=form.description.data
        )

        # Save the support group to the database
        db.session.add(support_group)
        db.session.commit()

        flash('Support group created successfully', 'success')
        return redirect(url_for('index'))

    return render_template('create_support_group.html', form=form)


@app_routes.route('/support-group', methods=['GET', 'POST'])
def support_groups():
    if request.method == 'POST':
        search_term = request.form.get('search')
        support_groups = SupportGroup.query.filter(
            SupportGroup.title.like(f'%{search_term}%')).all()
    else:
        support_groups = SupportGroup.query.all()

    return render_template('support_group.html', support_groups=support_groups)




api_routes = Blueprint('api_routes', __name__)

# API endpoint for joining a support group
@api_routes.route('/support-groups/<int:group_id>/join', methods=['POST'])
@login_required
def api_join_support_group(group_id):
    group = SupportGroup.query.get(group_id)

    if group:
        if current_user not in group.members:
            group.members.append(current_user)
            db.session.commit()
            return jsonify({'message': 'You have joined the support group.'}), 200
        else:
            return jsonify({'message': 'You are already a member of the support group.'}), 400
    else:
        return jsonify({'message': 'Support group not found.'}), 404

# API endpoint for leaving a support group
@api_routes.route('/support-groups/<int:group_id>/leave', methods=['POST'])
@login_required
def api_leave_support_group(group_id):
    group = SupportGroup.query.get(group_id)

    if group:
        if current_user in group.members:
            group.members.remove(current_user)
            db.session.commit()
            return jsonify({'message': 'You have left the support group.'}), 200
        else:
            return jsonify({'message': 'You are not a member of the support group.'}), 400
    else:
        return jsonify({'message': 'Support group not found.'}), 404


@api_routes.route('/forum/create', methods=['GET', 'POST'])
@app_routes.route('/forum/create', methods=['GET', 'POST'])
@login_required
def create_forum_post():
    form = ForumPostForm()
    if form.validate_on_submit():
        # Create a new ForumPost instance
        forum_post = ForumPost(title=form.title.data,
                               content=form.content.data, user=current_user)
        # Save the forum post to the database
        db.session.add(forum_post)
        db.session.commit()

        flash('Forum post created successfully!', 'success')

        # Redirect the user to the forum post detail page or forum listing page
        return redirect(url_for('forum_routes.forum_post_detail', post_id=forum_post.id))

    return render_template('create_forum_post.html', form=form)


@api_routes.route('/forum/posts', methods=['POST'])
@jwt_required
def create_forum_post():
    form = ForumPostForm()

    if form.validate_on_submit():
        # Create a new forum post
        forum_post = ForumPost(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(forum_post)
        db.session.commit()

        return jsonify(message='Forum post created successfully')

    return jsonify(errors=form.errors), 400


@api_routes.route('/forum/posts/<int:post_id>', methods=['PUT'])
@jwt_required
def update_forum_post(post_id):
    form = ForumPostForm()

    if form.validate_on_submit():
        # Find the forum post by post_id and check if the current user is the author
        forum_post = ForumPost.query.get_or_404(post_id)
        if forum_post.user_id != current_user.id:
            return jsonify(message='Unauthorized'), 403

        # Update the forum post
        forum_post.title = form.title.data
        forum_post.content = form.content.data
        db.session.commit()

        return jsonify(message='Forum post updated successfully')

    return jsonify(errors=form.errors), 400


@api_routes.route('/forum/posts/<int:post_id>', methods=['DELETE'])
@jwt_required
def delete_forum_post(post_id):
    # Find the forum post by post_id and check if the current user is the author
    forum_post = ForumPost.query.get_or_404(post_id)
    if forum_post.user_id != current_user.id:
        return jsonify(message='Unauthorized'), 403

    # Delete the forum post
    db.session.delete(forum_post)
    db.session.commit()

    return jsonify(message='Forum post deleted successfully')


@app_routes.route('/forum')
def forum_posts():
    # Retrieve all forum posts from the database
    page = request.args.get('page', 1, type=int)
    per_page = 10
    sorting = request.args.get('sort', 'date', type=str)
    category = request.args.get('category', type=str)

    query = ForumPost.query

    if category:
        query = query.filter_by(category=category)

    if sorting == 'date':
        query = query.order_by(ForumPost.created_at.desc())
    elif sorting == 'title':
        query = query.order_by(ForumPost.title.asc())
    elif sorting == 'comments':
        query = query.order_by(ForumPost.num_comments.desc())

    forum_posts = query.paginate(page=page, per_page=per_page)

    return render_template('forum_posts.html', posts=forum_posts, sorting=sorting, category=category)


@app_routes.route('/forum/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    like = PostLike.query.filter_by(
        user_id=current_user.id, post_id=post_id).first()

    if like:
        # User has already liked the post, remove the like
        db.session.delete(like)
        db.session.commit()
        flash('You unliked the post.', 'success')
    else:
        # User has not liked the post, add the like
        like = PostLike(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        flash('You liked the post.', 'success')

    return redirect(url_for('app_routes.forum_post_detail', post_id=post_id))


# Create comment route
@app_routes.route('/forum/posts/<post_id>/comments/create', methods=['GET', 'POST'])
@login_required
def create_comment(post_id):
    form = CommentForm()
    post = ForumPost.query.get(post_id)

    if form.validate_on_submit():
        comment = Comment(content=form.content.data,
                          post_id=post.id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment created successfully!', 'success')
        return redirect(url_for('forum_post', post_id=post.id))

    return render_template('create_comment.html', form=form, post=post)


@app_routes.route('/forum/posts/<post_id>/comments/<comment_id>/update', methods=['GET', 'POST'])
@login_required
def update_comment(post_id, comment_id):
    form = CommentForm()
    post = ForumPost.query.get(post_id)
    comment = Comment.query.get(comment_id)

    if comment.user != current_user:
        flash('You are not authorized to update this comment!', 'danger')
        return redirect(url_for('forum_post', post_id=post.id))

    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Comment updated successfully!', 'success')
        return redirect(url_for('forum_post', post_id=post.id))

    form.content.data = comment.content
    return render_template('update_comment.html', form=form, post=post, comment=comment)


@app_routes.route('/forum/posts/<post_id>/comments/<comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(post_id, comment_id):
    post = ForumPost.query.get(post_id)
    comment = Comment.query.get(comment_id)

    if comment.user != current_user:
        flash('You are not authorized to delete this comment!', 'danger')
        return redirect(url_for('forum_post', post_id=post.id))

    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('forum_post', post_id=post.id))
