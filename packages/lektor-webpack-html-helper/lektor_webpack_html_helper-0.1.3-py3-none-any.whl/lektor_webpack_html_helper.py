# -*- coding: utf-8 -*-
import os
import shutil

from lektor.pluginsystem import Plugin
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from lektor.reporter import CliReporter


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
        src_dir = self.env.root_path + '/' + (self.get_config().get('src_dir') or 'assets') + '/'
        target_dir = self.env.root_path + '/' + (self.get_config().get('target_dir') or 'templates') + '/'
        
        self.observer = Observer()
        self.handler = HtmlHandler(target=target_dir)
        self.observer.schedule(
            self.handler, src_dir, recursive=True
        )
        
        cli_reporter = CliReporter(self.env)
        cli_reporter.report_generic(f'Starting webpack-html helper: {src_dir} -> {target_dir}')

        self.observer.start()