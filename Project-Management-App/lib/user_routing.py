from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from lib import db, bcrypt
from lib.models import User, Tasks, Task_assignment, Project_assignment, Project
from lib.forms import RegistrationForm, LoginForm, UpdateAccountForm

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('project_routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("project_routes.index"))
    return render_template("login.html", form=form)


@user_routes.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('project_routes.index'))
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(email=form.email.data, password=hashed_pwd)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_routes.account"))
    return render_template("register.html", form=form)


@user_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user_routes.login'))


@user_routes.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.team = form.team.data
        current_user.position = form.position.data
        db.session.add(current_user)
        db.session.commit()
        # flash("Your account has been updated!", "success")
        return redirect(url_for('user_routes.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.team.data = current_user.team
        form.position.data = current_user.position
    return render_template('account.html', title='Account', form=form)

@user_routes.route('/assignments', methods=['GET', 'POST'])
@login_required
def assignments():
    if current_user.is_authenticated:
        # print("User id is: ", current_user.id)
        uid = int(current_user.id)
        # print("User id is: ", uid)
        my_tasks = Tasks.query.filter(Tasks.assigned_to==uid).all()
        ids = []
        for task in my_tasks:
            ids.append(task.id)

        my_incomplete_tasks = Tasks.query.filter(Tasks.id.in_(ids)).filter(Tasks.status != "Completed")
        my_completed_tasks = Tasks.query.filter(Tasks.id.in_(ids)).filter(Tasks.status == "Completed")
        my_projects = Project_assignment.query.filter(Project_assignment.user_id==uid).all()
        len_ = len(list(my_completed_tasks))
        pid = []
        for pr in my_projects:
            pid.append(pr.project_id)
        assigned_projects = Project.query.filter(Project.id.in_(pid)).all()
        print(my_projects)
        
    return render_template('my_stuff.html', incomplete = my_incomplete_tasks, complete = my_completed_tasks, len_=len_, projects = assigned_projects)
