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
from flask_menu.classy import register_flaskview

from .resource import Index

q_index = Blueprint('q_index', __name__, template_folder='templates')

class Plugin(object):

    def load(self, core):
        Index.register(q_index, route_base='/x/users', route_prefix='')
        register_flaskview(q_index, Index)
        core.register_blueprint(q_index)
