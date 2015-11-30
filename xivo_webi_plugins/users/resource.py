# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from contextlib import contextmanager
import logging

from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from xivo_confd_client.client import ConfdClient

from flask.ext.classy import FlaskView
from xivo_webi.auth import verify_token

from .forms import UserForm


logger = logging.getLogger(__name__)


@contextmanager
def new_confd_client(config):
    current_app.config['confd']['token'] = request.cookies.get('x-auth-session')
    yield ConfdClient(**config)


class Demo(FlaskView):
    decorators = [verify_token]

    def index(self):
        with new_confd_client(current_app.config['confd']) as confd:
            users = confd.users.list()
        return render_template('demo.html', users=users)

    def get(self, id):
        with new_confd_client(current_app.config['confd']) as confd:
            user = confd.users.get(id)
        form = UserForm(data=user)
        return render_template('demo_form.html', form=form)

    def post(self, id):
        form = UserForm()
        if form.validate_on_submit():
            with new_confd_client(current_app.config['confd']) as confd:
                user = { 'id': id,
                         'firstname': form.firstname.data,
                         'lastname' : form.lastname.data
                       }
                confd.users.update(user)
        return redirect(url_for('demo.Demo:index'))

class DemoAdd(FlaskView):
    decorators = [verify_token]

    def get(self):
        form = UserForm()
        return render_template('demo_form.html', form=form)

    def post(self):
        form = UserForm()
        if form.validate_on_submit():
            with new_confd_client(current_app.config['confd']) as confd:
                user = { 'firstname': form.firstname.data,
                         'lastname' : form.lastname.data
                       }
                confd.users.create(user)
        return redirect(url_for('demo.Demo:index'))

class DemoDelete(FlaskView):
    decorators = [verify_token]

    def get(self, id):
        with new_confd_client(current_app.config['confd']) as confd:
            confd.users.delete(id)
        return redirect(url_for('demo.Demo:index'))
