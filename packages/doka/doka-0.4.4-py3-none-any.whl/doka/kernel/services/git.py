#!/usr/bin/env python3
import subprocess
from doka.kernel.definition.entities import UnitEntity
import shutil


class Git:
    def __init__(self, unit: UnitEntity):
        self._unit = unit

    def clone(self, from_template=False):
        subprocess.run(
            "rm -rf {directory} && git clone {repo} {directory}/".format(
                repo=self._unit.repo,
                directory=self._unit.codedir
            ),
            shell=True,
            check=True)
        if from_template:
            shutil.rmtree('{}/.git'.format(self._unit.codedir))

    def init(self):
        subprocess.run(
            "cd {directory} && git init && git add readme.md && git commit -m 'Initial commit' ".format(
                directory=self._unit.codedir),
            shell=True,
            check=True
        )

    def add_origin(self, push_initial_commit=False):
        subprocess.run(
            "cd {directory} && git remote add origin {repo} {initial_commit}".format(
                directory=self._unit.codedir, repo=self._unit.repo,
                initial_commit='&& git push origin master' if push_initial_commit else ''
            ),
            shell=True,
            check=True
        )

    def checkout(self, branch, force=False):
        subprocess.run("cd {directory} && git checkout {force} {branch}".format(
            directory=self._unit.codedir,
            force='-b' if force else '',
            branch=branch
        ), shell=True, check=True)

    def fetch(self, force=True):
        subprocess.run("cd {directory} && git fetch {force}".format(
            directory=self._unit.codedir,
            force='&& git reset --hard origin/development' if force else ''
        ), shell=True, check=True)

    def pull(self):
        subprocess.run("cd {directory} && git pull origin {branch}".format(
            directory=self._unit.codedir,
            branch=self.get_branch()
        ), shell=True, check=True)

    def get_branch(self):
        return subprocess.check_output(
            "cd {directory} && git rev-parse --abbrev-ref HEAD".format(directory=self._unit.codedir),
            shell=True).decode().strip()

    def commit(self, message=''):
        subprocess.run("cd {directory} && git add . && git commit -m \"{message}\"".format(
            directory=self._unit.codedir,
            message=message
        ), shell=True, check=True)

    def merge(self, dst_branch):
        subprocess.run("cd {directory} && git checkout {dst_branch} && git merge {src_branch}".format(
            directory=self._unit.codedir,
            dst_branch=dst_branch,
            src_branch=self.get_branch()
        ), shell=True, check=True)

    def push(self):
        subprocess.run("cd {directory} && git push origin {branch}".format(
            directory=self._unit.codedir,
            branch=self.get_branch()
        ), shell=True, check=True)
