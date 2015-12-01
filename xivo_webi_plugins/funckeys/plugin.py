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
from flask.ext.menu.classy import register_flaskview

from .resource import FK

q_fk = Blueprint('q_fk', __name__, template_folder='templates',
                 static_folder='static', static_url_path='/%s' % __name__)

class Plugin(object):

    def load(self, core):
        FK.register(q_fk, route_base='/x/fk', route_prefix='')
        register_flaskview(q_fk, FK)
        core.register_blueprint(q_fk)
        self.configure(core)

    def configure(self, core):
        core.config['ctid'] = dict()
        core.config['ctid']['host'] = '192.168.1.124'

        core.config['ws'] = dict()
        core.config['ws']['host'] = '192.168.1.124'
