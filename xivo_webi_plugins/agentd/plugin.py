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

from .resource import Agentd
from .resource import AgentdAction

q_agentd = Blueprint('q_agentd', __name__, template_folder='templates',
                     static_folder='static', static_url_path='/%s' % __name__)

class Plugin(object):

    def load(self, core):
        Agentd.register(q_agentd, route_base='/x/agentd', route_prefix='')
        AgentdAction.register(q_agentd, route_base='/x/agentd', route_prefix='')
        register_flaskview(q_agentd, Agentd)
        core.register_blueprint(q_agentd)
        self.configure_agentd(core)

    def configure_agentd(self, core):
        core.config['agentd'] = dict()
        core.config['agentd']['host'] = "192.168.1.124"
        core.config['agentd']['verify_certificate'] = False

        core.config['rabbitmq'] = dict()
        core.config['rabbitmq']['host'] = "192.168.1.124"
        core.config['rabbitmq']['port'] = 15675
        core.config['rabbitmq']['scheme'] = "https"
        core.config['rabbitmq']['username'] = "xivo"
        core.config['rabbitmq']['password'] = "xivo"
