from lib import db, login_manager
from flask import current_app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    status = db.Column(db.String)
    date_added = db.Column(db.String)
    added_by = db.Column(db.String)
    tasks = db.relationship("Tasks", backref='project')
    assignment = db.relationship("Project_assignment", backref='project')
    notes = db.relationship("Note", backref='project')
    resources = db.relationship("Resources", backref='project')


class Project_assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    assigned_teammate = db.Column(db.String)
    email = db.Column(db.String)
    date_added = db.Column(db.String)
    assigned_by = db.Column(db.String)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    # possible statuses: idle, in progress, completed
    status = db.Column(db.String)
    # three datetime needed: date of adding to db, due date and complete date;
    date_added = db.Column(db.String)
    due_date = db.Column(db.String)
    date_completed = db.Column(db.String)
    # one more column needed for the person assigned to the task;
    assigned_to = db.Column(db.String) #user name
    # low/medium/high values allowed
    importance = db.Column(db.String)
    # project to which the task is related to
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    # creating a relation to Task_assignment model
    assignment = db.relationship("Task_assignment",backref="tasks")

class Task_assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    assigned_fname = db.Column(db.String)
    assigned_lname = db.Column(db.String)
    email = db.Column(db.String)
    date_added = db.Column(db.String)
    assigned_by = db.Column(db.String)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    team = db.Column(db.String)
    position = db.Column(db.String)
    assignment = db.relationship('Project_assignment', backref='user')



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    date_added = db.Column(db.String)
    added_by = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))


class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    content = db.Column(db.String)
    date_added = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
