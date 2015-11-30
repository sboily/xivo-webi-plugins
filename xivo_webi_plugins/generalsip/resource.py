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

from flask import render_template, redirect, url_for
from flask.ext.classy import FlaskView

import models as generalsip_dao
from forms import FormGeneralSIP

from xivo_webi.auth import verify_token

logger = logging.getLogger(__name__)


class GeneralSIP(FlaskView):
    decorators = [verify_token]

    def get(self):
        sip = generalsip_dao.list()
        form = FormGeneralSIP(obj=sip)
        return render_template('generalsip.html', form=form)

    def post(self):
        sip = generalsip_dao.list()
        form = FormGeneralSIP(obj=sip)
        if form.validate_on_submit():
            form.populate_obj(sip)
            generalsip_dao.edit(sip)
        return redirect(url_for("generalsip.index"))