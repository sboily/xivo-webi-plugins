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

from flask import render_template
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask.ext.classy import FlaskView

from xivo_webi.auth import verify_token
from xivo_dao.helpers.db_utils import session_scope

import models as meetme_dao
from .forms import MeetmeForm

logger = logging.getLogger(__name__)


class Meetme(FlaskView):
    decorators = [verify_token]

    def index(self):
        with session_scope():
            meetme = meetme_dao.list()
            return render_template('meetme.html', meetme=meetme)

    def get(self, id):
        with session_scope():
            meetme = meetme_dao.get(id)
            form = MeetmeForm(obj=meetme)
            return render_template('meetme_form.html', form=form)

    def post(self, id):
        with session_scope():
            meetme = meetme_dao.get(id)
            form = MeetmeForm(obj=meetme)
            if form.validate_on_submit():
                form.populate_obj(meetme)
                meetme_dao.edit(meetme)
        return redirect(url_for('meetme.Meetme:index'))

class MeetmeAdd(FlaskView):
    decorators = [verify_token]

    def get(self):
        form = MeetmeForm()
        return render_template('meetme_form.html', form=form)

    def post(self):
        form = MeetmeForm()
        if form.validate_on_submit():
            with session_scope():
                meetme_dao.add(form)
        return redirect(url_for('meetme.Meetme:index'))

class MeetmeDelete(FlaskView):
    decorators = [verify_token]

    def get(self, id):
        with session_scope():
            meetme_dao.delete(id)
        return redirect(url_for('meetme.Meetme:index'))
