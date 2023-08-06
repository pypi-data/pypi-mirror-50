# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import shutil


class HtmlHandler(PatternMatchingEventHandler):
    patterns = ["*/*.html"]

    def __init__(self, target, *args, **kwargs):
        self.target = target
        return super().__init__(*args, **kwargs)

    def on_any_event(self, event):
        self.path, self.filename = os.path.split(event.src_path)

    def on_modified(self, event):
        shutil.copyfile(event.src_path, self.target + self.filename)

    def on_created(self, event):
        self.on_modified(event)

    def on_deleted(self, event):
        if os.path.exists(self.target + self.filename):
            os.remove(self.target + self.filename)


class WebpackHtmlHelperPlugin(Plugin):
    name = "lektor-webpack-html-helper"
    description = u"Observes the assets directory for html files and copies them into the templates folder."

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.observer = Observer()
        self.handler = HtmlHandler(target=self.env.root_path + "/templates/")

    def on_server_spawn(self, **extra):
        self.observer.schedule(
            self.handler, self.env.root_path + "/assets/", recursive=True
        )
        self.observer.start()

    def on_server_stop(self, **extra):
        self.observer.stop()
        self.observer.join()
