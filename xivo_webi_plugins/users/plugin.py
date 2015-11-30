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

from flask import Blueprint

from .resource import Demo
from .resource import DemoAdd
from .resource import DemoDelete

demo = Blueprint('demo', __name__, template_folder='templates')

class Plugin(object):

    def load(self, core):
        Demo.register(demo, route_base='/', route_prefix='/x/demo')
        DemoAdd.register(demo, route_base='/add', route_prefix='/x/demo')
        DemoDelete.register(demo, route_base='/delete', route_prefix='/x/demo')
        core.register_blueprint(demo)

