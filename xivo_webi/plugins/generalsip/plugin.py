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

from flask import Blueprint
import xivo_dao

from .resource import GeneralSIP

q_generalsip = Blueprint('q_generalsip', __name__, template_folder='templates'
                         static_folder='static', static_url_path='/%s' % __name__)

class Plugin(object):

    def load(self, core):
        xivo_dao.init_db_from_config(core.config)
        GeneralSIP.register(q_generalsip, route_base='/x/generalsip', route_prefix='')
        core.register_blueprint(q_generalsip)
