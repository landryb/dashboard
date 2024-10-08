#!/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

from flask import Blueprint
from flask import request, render_template
from flask import current_app as app
from geordash.decorators import is_superuser

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder='templates')

@admin_bp.route("/")
def index() -> str:
    all_jobs_for_msconfigs = app.extensions['rcli'].get_taskids_by_taskname_and_args('geordash.checks.mapstore.check_configs',[])
    all_jobs_for_msresources = app.extensions['rcli'].get_taskids_by_taskname_and_args('geordash.checks.mapstore.check_resources',[])
    # cf https://github.com/pallets/flask/issues/1361
    # and https://flask.palletsprojects.com/en/3.0.x/blueprints/#templates
    return render_template("admin/index.html", previous_configs_jobs=all_jobs_for_msconfigs, previous_resources_jobs=all_jobs_for_msresources, bootstrap=app.extensions["bootstrap"], showdelete=is_superuser())
