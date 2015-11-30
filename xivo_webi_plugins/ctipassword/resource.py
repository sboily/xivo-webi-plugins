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

import logging

from flask import render_template, current_app, redirect, url_for
from xivo_confd_client.client import ConfdClient
from forms import FormCTIPassword
from contextlib import contextmanager
from flask.ext.classy import FlaskView

from xivo_webi.auth import verify_token
from xivo_webi.auth import current_user

from flask_menu.classy import classy_menu_item

logger = logging.getLogger(__name__)


@contextmanager
def confd_client(config):
    yield ConfdClient(**config)

class CTIPassword(FlaskView):
    decorators = [verify_token]

    @classy_menu_item('q_ctipassword', 'CTIPASS', order=0)
    def get(self):
        form=FormCTIPassword()
        return render_template('ctipassword.html',form=form)

    def post(self):
        form=FormCTIPassword()
        if form.validate_on_submit():
            user = dict(id=current_user.get_uuid(),password=form.data['password'])
            with confd_client(current_app.config['confd']) as confd:
                try:
                    confd.users.update(user)
                    return redirect(url_for('q_ctipassword.CTIPassword:get'))
                except:
                    print "Error to update user password"
        return render_template('ctipassword.html',form=form)
