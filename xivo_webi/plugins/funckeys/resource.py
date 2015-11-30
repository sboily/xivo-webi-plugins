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

from flask import render_template, current_app
from flask.ext.classy import FlaskView
from contextlib import contextmanager

from xivo_confd_client import Client as confd_client
from xivo_ctid_client import Client as ctid_client

logger = logging.getLogger(__name__)


@contextmanager
def new_confd_client(config):
    current_app.config['confd']['token'] = request.cookies.get('x-auth-session')
    yield confd_client(**config)

@contextmanager
def new_ctid_client(config):
    yield ctid_client(**config)


class FK(object):
    decorators = [verify_token]

    def index(self):
        current_user.user_id = "TODO XXX"
        with new_confd_client(current_app.config['confd']) as confd:
            fk = gen_template_fk(confd, confd.users.relations(current_user.user_id).list_funckeys())
        return render_template('fk.html', fk=fk, ws=current_app.config['ws'])

def gen_template_fk(confd, fk):
   template = dict()
   fk_keys = fk['keys']

   for f in fk_keys:
      id = fk_keys[f]['id']
      label = fk_keys[f]['label']
      blf = fk_keys[f]['blf']
      inherited = fk_keys[f]['inherited']
      destination = get_destination(confd, fk_keys[f])
      if destination:
          line = get_line(confd, fk_keys[f]['destination']['user_id'])

          template.update({id: dict(label=label,
                                    blf=blf,
                                    inherited=inherited,
                                    line=line,
                                    endpoint_status=get_endpoint_status(line),
                                    destination=destination)
                         })

   return template

def get_destination(confd, fk_keys):
    fk_type = fk_keys['destination']['type']
    destination = False

    if fk_type == 'user':
        id = fk_keys['destination']['user_id']
        user = confd.users.get(id)
        destination = "%s %s" %(user['firstname'],
                                user['lastname'])
    return destination

def get_line(confd, user_id):
    lines = confd.users.relations(user_id).list_lines()
    line = lines['items'][0]['line_id']
    return line

def get_endpoint_status(endpoint_id):
    with new_ctid_client(current_app.config['ctid']) as cti:
        endpoint_status = cti.endpoints.get(endpoint_id)
        return endpoint_status['status']
    return False
