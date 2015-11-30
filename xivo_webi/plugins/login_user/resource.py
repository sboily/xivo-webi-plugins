# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Sylvain Boily
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


import logging
from contextlib import contextmanager

from flask import render_template, redirect, url_for, current_app, make_response
from flask.ext.classy import FlaskView

from xivo_auth_client import Client as client_auth
from xivo_confd_client import Client as client_confd

from forms import LoginUserForm

logger = logging.getLogger(__name__)


@contextmanager
def new_confd_client(config):
    yield client_confd(**config)

@contextmanager
def new_auth_client(config):
    yield client_auth(**config)


class LoginUser(FlaskView):

    def get(self):
        form = LoginUserForm()
        session = request.cookies.get("x-auth-session")
        host = request.host

        if session:
            return redirect('https://{}'.format(host))
        return render_template('login.html', form=form)

    def post(self):
        form = LoginUserForm()

        if form.validate_on_submit():
            host = request.host
            current_app.config['auth']['username'] = form.username.data
            current_app.config['auth']['password'] = form.password.data

            with xivo_auth(current_app.config['auth']) as auth:
                token_data = auth.token.new('xivo_user', expiration=3600)
                if not token_data:
                    return redirect(url_for('login_user.LoginUser:get'))
                token = token_data['token']

            if token:
                redirect_to_index = redirect('https://{}'.format(host))
                response = make_response(redirect_to_index)
                response.set_cookie('x-auth-session', token)

                return response
        return render_template('login.html', form=form)


class LogoutUser(FlaskView):
    decorators = [verify_token]

    def get(self):
        session = request.cookies.get("x-auth-session")

        if session:
            with xivo_auth(current_app.config['auth']) as auth:
                auth.token.revoke(session)

        response = redirect(url_for('login_user.LoginUser:get'))
        response.set_cookie('x-auth-session', '', expires=0)

        return response
