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
from flask.ext.menu.classy import classy_menu_item

import models as generalsip_dao
from forms import FormGeneralSIP
from utils import convertToSIPToDict

from xivo_webi.auth import verify_token
from xivo_dao.helpers.db_utils import session_scope

logger = logging.getLogger(__name__)


class GeneralSIP(FlaskView):
    decorators = [verify_token]

    @classy_menu_item('q_generalsip', 'SIP', order=0)
    def get(self):
        with session_scope():
            sip = convertToSIPToDict(generalsip_dao.list())
            form = FormGeneralSIP(obj=sip)
            return render_template('generalsip.html', form=form)

    def post(self):
        with session_scope():
            sip = generalsip_dao.list()
            form = FormGeneralSIP(obj=sip)
            if form.validate_on_submit():
                form.populate_obj(sip)
                generalsip_dao.edit(sip)
        return redirect(url_for("generalsip:GeneralSIP:get"))
