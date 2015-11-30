# -*- coding: UTF-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from xivo_dao.alchemy.meetmefeatures import MeetmeFeatures
from xivo_dao.alchemy.staticmeetme import StaticMeetme
from xivo_dao.alchemy.extension import Extension
from xivo_dao.helpers.db_manager import daosession

@daosession
def list(session):
    return (session.query(MeetmeFeatures)
            .all()
           )

@daosession
def get(session, id):
    return _get_meetme(id)

@daosession
def add(session, form):
    staticmeetme = _add_static(form.confno.data)
    session.add(staticmeetme)
    session.commit()

    meetme = _add_meetme(form, staticmeetme.id)
    session.add(meetme)
    session.commit()

    extension = _add_extension(meetme.confno, meetme.context, meetme.id)
    session.add(extension)

@daosession
def delete(session, id):
    meetme = _get_meetme(id)
    staticmeetme = _get_staticmeetme(meetme.confno)
    extension = _get_extension(meetme.id)

    session.delete(meetme)
    session.delete(staticmeetme)
    session.delete(extension)

@daosession
def edit(session, meetme):
    extension = _get_extension(meetme.id)
    staticmeetme = _get_staticmeetme(extension.exten)

    extension.exten = meetme.confno
    extension.context = meetme.context

    staticmeetme.var_val = _get_exten_pin(staticmeetme.var_val)

    session.add(extension)
    session.add(staticmeetme)
    session.add(meetme)


@daosession
def _get_meetme(session, id):
    meetme = (session.query(MeetmeFeatures)
              .filter(MeetmeFeatures.id == id)
              .first()
             )

    return meetme

@daosession
def _get_staticmeetme(session, exten):
    staticmeetme = (session.query(StaticMeetme)
                    .filter(StaticMeetme.var_val.like(exten+"%"))
                    .filter(StaticMeetme.var_name == 'conf')
                    .first()
                   )

    return staticmeetme

@daosession
def _get_extension(session, meetmeid):
    extension = (session.query(Extension)
                 .filter(Extension.typeval == str(meetmeid))
                 .filter(Extension.type == 'meetme')
                 .first()
                )

    return extension

def _add_meetme(form, staticmeetmeid):
    meetme = MeetmeFeatures()

    meetme.meetmeid = staticmeetmeid
    meetme.name = form.name.data
    meetme.confno = form.confno.data
    meetme.context = form.context.data
    meetme.admin_identification = 'pin'
    meetme.admin_mode = 'all'
    meetme.admin_announcejoinleave = 'no'
    meetme.user_mode = 'all'
    meetme.user_announcejoinleave = 'no'
    meetme.emailbody = ''
    meetme.description = form.description.data

    return meetme

def _add_static(exten):
    staticmeetme = StaticMeetme()

    staticmeetme.cat_metric = 1
    staticmeetme.filename = 'meetme.conf'
    staticmeetme.category = 'rooms'
    staticmeetme.var_name = 'conf'
    staticmeetme.var_val = exten

    return staticmeetme

def _add_extension(exten, context, meetmeid):
    extension = Extension()

    extension.exten = exten
    extension.context = context
    extension.typeval = meetmeid
    extension.type = 'meetme'

    return extension

def _get_exten_pin(exten_pin):
    val = exten_pin.split(',')
    if len(val) > 1:
        return "{},{}".format(val[0], val[1])
    return exten_pin

