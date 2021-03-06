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
from flask.ext.classy import FlaskView
from flask_menu.classy import classy_menu_item

from xivo_webi.auth import verify_token

logger = logging.getLogger(__name__)


class Index(FlaskView):
    decorators = [verify_token]

    @classy_menu_item('.main', 'Home', order=0)
    def index(self):
        return render_template('index_user.html')
