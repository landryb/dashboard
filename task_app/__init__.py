#!/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

from celery import Celery
from celery import Task
from flask import Flask
from flask import render_template

from threading import Thread
from config import url

# this celery app object is used by the beat and worker threads
capp = Celery(__name__)
capp.config_from_object('task_app.celeryconfig')
capp.set_default()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=capp.conf
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    from . import views

    app.register_blueprint(views.bp)
    return app

def beat_thread():
    capp.Beat(loglevel='info').run()

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    tbeat = Thread(name='beat',target=beat_thread)
    tbeat.start()
    return celery_app
