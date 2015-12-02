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

from flask import render_template, current_app, redirect, url_for, request
from xivo_agentd_client.client import AgentdClient
from contextlib import contextmanager
from flask.ext.classy import FlaskView

from xivo_webi.auth import verify_token
from xivo_webi.auth import current_user
from xivo_webi.auth import get_service_token

from flask_menu.classy import classy_menu_item

from forms import FormAgentd

logger = logging.getLogger(__name__)


@contextmanager
def agentd_client(config):
    yield AgentdClient(**config)

class Agentd(FlaskView):
    decorators = [verify_token]

    @classy_menu_item('.agentd', 'Agentd', order=0)
    @classy_menu_item('.agentd.panel', 'Dashboard', order=0)
    @get_service_token
    def get(self):
        form=FormAgentd()
        current_app.config['agentd']['token'] = current_app.config['service_token']
        with agentd_client(current_app.config['agentd']) as agentd:
            agents = agentd.agents.get_agent_statuses()
        return render_template('agentd.html',form=form, agents=agents, rabbitmq=current_app.config['rabbitmq'])

class AgentdAction(FlaskView):
    #decorators = [verify_token]

    @get_service_token
    def get(self, id):
        current_app.config['agentd']['token'] = current_app.config['service_token']
        with agentd_client(current_app.config['agentd']) as agentd:
            agentd.agents.logoff_agent(id)
        return '', 200

    @get_service_token
    def post(self, id):
        extension = request.form.get('extension')
        context = request.form.get('context')
        current_app.config['agentd']['token'] = current_app.config['service_token']
        with agentd_client(current_app.config['agentd']) as agentd:
            agentd.agents.login_agent(id, extension, context)
        return '', 200
