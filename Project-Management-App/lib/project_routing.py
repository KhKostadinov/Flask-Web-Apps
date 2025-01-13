from flask import render_template, request, redirect, url_for, flash, Blueprint
from lib import db
from lib.models import Project, Tasks, Resources, User, Project_assignment
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required

project_routes = Blueprint("project_routes", __name__)


@project_routes.route("/projects", methods = ["GET","POST"])
@login_required
def index():
    projects = Project.query.all()
    if request.method == "POST":
        srch = str(request.form["search"])
        searched_projects = Project.query.filter(Project.name.contains(srch)).all()
        return render_template("search.html", searched_projects=searched_projects)
    return render_template("projects.html", projects=projects)


@project_routes.route('/project/<int:project_id>')
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    incomplete_tasks = Tasks.query.filter_by(project=project).filter(Tasks.status != "Completed").order_by(Tasks.due_date.desc()).all()
    complete_tasks = Tasks.query.filter_by(project=project).filter(Tasks.status == "Completed").order_by(Tasks.due_date.desc()).all()
    resources = Resources.query.filter_by(project=project).all()
    team = User.query.filter(User.id > 1)
    assigned = Project_assignment.query.filter_by(project=project)
    return render_template("tasks.html", project=project, incomplete=incomplete_tasks, complete=complete_tasks,
                           resources=resources, team=team, assigned=assigned)


@project_routes.route("/add_project", methods=["GET", "POST"])
@login_required
def add():
    now = datetime.now()
    date_string = now.strftime("%Y/%m/%d %H:%M")
    team = User.query.all()
    if request.method == "POST":
        project = Project(name=request.form['projectname'], description=request.form["projectdescription"],
                     status=request.form['projectstatus'], date_added=date_string)
        usid = request.form['teammate']
        
        # return usid
        if usid != "Assign:": 
            m1 = User.query.get_or_404(usid)
            mate_ = Project_assignment(user_id=m1.id, date_added=date_string, project=project, email=m1.email,
                                    assigned_teammate=m1.fname)
        # else:
        #     m1 = User.query.get_or_404(1)
        #     mate_ = Project_assignment(user_id=m1.id, date_added=date_string, project=project, email=m1.email,
        #                             assigned_teammate=m1.lname)
        db.session.add(mate_)
        db.session.add(project)
        db.session.commit()
        # return redirect(url_for("project_routes.index"))
        return redirect(url_for("project_routes.project", project_id=project.id))
    return render_template("addproject.html", team = team)
    # return redirect(url_for("index"))


@project_routes.route('/project/<int:project_id>/edit', methods=["GET", "POST"])
@login_required
def edit(project_id):
    now = datetime.now()
    date_string = now.strftime("%Y/%m/%d %H:%M")
    project = Project.query.get_or_404(project_id)
    team = User.query.all()
    if request.method == "POST":
        project.title = request.form["projectname"]
        project.description = request.form["projectdescription"]
        project.status = request.form["projectstatus"]
        usid = request.form['teammate']
        if usid != "Assign:": 
            m1 = User.query.get_or_404(usid)
            mate_ = Project_assignment(user_id=m1.id, date_added=date_string, project=project, email=m1.email,
                                    assigned_teammate=m1.fname)
        # else:
        #     m1 = User.query.get_or_404(1)
        #     mate_ = Project_assignment(user_id=m1.id, date_added=date_string, project=project, email=m1.email,
        #                             assigned_teammate=m1.lname)
        db.session.add(mate_)
        db.session.add(project)
        db.session.commit()
        flash("Project updated!")
        return redirect(url_for("project_routes.project", project_id=project.id))
    return render_template("addproject.html", project=project, team=team)


