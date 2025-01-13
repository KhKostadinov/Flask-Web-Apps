from flask import render_template, request, redirect, url_for, flash, Blueprint
from lib import db
from lib.models import Tasks, Project, User, Task_assignment
from datetime import datetime

task_routes = Blueprint("task_routes", __name__)


@task_routes.route("/add/<int:project_id>", methods=["GET", "POST"])
def add(project_id):
    now = datetime.now()
    date_string = now.strftime("%Y/%m/%d %H:%M")
    proj = Project.query.get_or_404(project_id)
    team = User.query.all()
    if request.method == "POST":
        task = Tasks(title=request.form['tasktitle'], description=request.form["taskdescription"],
                        status=request.form['taskstatus'], date_added=date_string, due_date=request.form["duedate"],
                        importance=request.form["importance"], assigned_to=request.form["teammate"],project=proj)
        # assignment = Task_assignment(task_id=task.id,user_id=m1.id,assigned_fname=m1.fname,assigned_lname=m1.lname,email=m1.email)
        if task.status == "Completed":
            task.date_completed = date_string
        db.session.add(task)
        # db.session.add(assignment)
        db.session.commit()
        return redirect(url_for("project_routes.project", project_id=proj.id,task=task,team=team))
        
    return render_template("addtask.html", project=proj, team=team)


@task_routes.route('/task/<int:task_id>/edit', methods=["GET", "POST"])
def edit(task_id):
    now = datetime.now()
    date_string = now.strftime("%Y/%m/%d %H:%M")
    task = Tasks.query.get_or_404(task_id)
    project = Project.query.get_or_404(task.project_id)
    team = User.query.all()
    assig = User.query.get_or_404(task.assigned_to)
    if request.method == "POST":
        task.title = request.form["tasktitle"]
        task.description = request.form["taskdescription"]
        task.status = request.form["taskstatus"]
        task.due_date = request.form["duedate"]
        task.importance = request.form["importance"]
        task.assigned_to = request.form["teammate"]
        # assignment = Task_assignment(task_id=task.id, user_id=assigned.id, assigned_fname=assigned.fname, assigned_lname=assigned.lname, 
        # email=assigned.email, date_added=date_string)
        if task.status == "Completed":
            task.date_completed = date_string
        db.session.add(task)
        # db.session.add(assignment)
        db.session.commit()
        flash("Task updated!")
        return redirect(url_for("project_routes.project", project_id=project.id, task=task, team=team, assig=assig))
    return render_template("addtask.html", project=project, task=task, team=team, assig=assig)


@task_routes.route('/task/<int:task_id>/delete', methods=["POST"])
def delete_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    # assig = Task_assignment.query.filter_by(task_id = task.id).all()
    project = Project.query.get_or_404(task.project_id)

    if request.method == "POST":
        db.session.delete(task)
        # db.session.delete(assig)
        db.session.commit()
        flash("Task deleted!")
        return redirect(url_for("project_routes.project", project_id=project.id, task=task))
