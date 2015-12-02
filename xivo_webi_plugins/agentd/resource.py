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
from contextlib import contextmanager
from flask.ext.classy import FlaskView

from xivo_webi.auth import verify_token
from xivo_webi.auth import current_user
from xivo_webi.auth import get_service_token

from flask_menu.classy import classy_menu_item

logger = logging.getLogger(__name__)


@contextmanager
def confd_client(config):
    yield ConfdClient(**config)

class Agentd(FlaskView):
    decorators = [verify_token]

    @classy_menu_item('.agentd', 'CTI', order=0)
    @classy_menu_item('.agentd.panel', 'Dashboard', order=0)
    def get(self):
        form=FormCTIPassword()
        return render_template('agentd.html',form=form)
