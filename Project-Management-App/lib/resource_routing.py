from flask import render_template, request, redirect, url_for, flash, Blueprint
from lib import db
from lib.models import Project, Resources, Project_assignment, User
from datetime import datetime

resource_routes = Blueprint("resource_routes", __name__)


@resource_routes.route("/add_res/<int:project_id>", methods=["GET", "POST"])
def add_res(project_id):
    now = datetime.now()
    date_string = now.strftime("%Y/%m/%d")
    proj = Project.query.get_or_404(project_id)
    if request.method == "POST":
        resource = Resources(label=request.form['resourcelabel'], content=request.form["resourcelink"],
                             date_added=date_string, project=proj)
        db.session.add(resource)
        db.session.commit()
        return redirect(url_for("project_routes.project", project_id=proj.id))
    return render_template("addresource.html", project=proj)
    # return redirect(url_for("index"))


@resource_routes.route('/resource/<int:resource_id>/edit', methods=["GET", "POST"])
def edit(resource_id):
    resource = Resources.query.get_or_404(resource_id)
    project = Project.query.get_or_404(resource.project_id)
    if request.method == "POST":
        resource.label = request.form["resourcelabel"]
        resource.content = request.form["resourcelink"]
        db.session.commit()
        flash("Resource updated!")
        return redirect(url_for("project_routes.project", project_id=project.id, resource=resource))
    return render_template("tasks.html", project=project, resource=resource)


@resource_routes.route('/resource/<int:resource_id>/delete', methods=["POST"])
def delete_resource(resource_id):
    resource = Resources.query.get_or_404(resource_id)
    project = Project.query.get_or_404(resource.project_id)
    if request.method == "POST":
        db.session.delete(resource)
        db.session.commit()
        flash("Resource deleted!")
        return redirect(url_for("project_routes.project", project_id=project.id, resource=resource))


@resource_routes.route("/assign/<int:project_id>", methods=["GET", "POST"])
def assign(project_id):
    now = datetime.now()
    date_string = now.strftime("%Y/%m/%d")
    proj = Project.query.get_or_404(project_id)
    team = User.query.all()
    if request.method == "POST":
        usid = request.form['assigned']
        m1 = User.query.get_or_404(usid)
        mate_ = Project_assignment(user_id=m1.id, date_added=date_string, project=proj, email=m1.email,
                                   assigned_teammate=m1.fname)

        db.session.add(mate_)
        db.session.commit()
        return redirect(url_for("project_routes.project", project_id=proj.id))
    return render_template("tasks.html", project=proj, team=team)


@resource_routes.route('/assign/<int:assignment_id>/delete', methods=["POST"])
def delete_assigned(assignment_id):
    assig = Project_assignment.query.get_or_404(assignment_id)
    project = Project.query.get_or_404(assig.project_id)
    if request.method == "POST":
        db.session.delete(assig)
        db.session.commit()
        flash("Resource deleted!")
        return redirect(url_for("project_routes.project", project_id=project.id, assig=assig))
