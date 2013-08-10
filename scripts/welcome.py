# Copyright (c) Mathias Kaerlev 2013.
#
# This file is part of cuwo.
#
# cuwo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cuwo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cuwo.  If not, see <http://www.gnu.org/licenses/>.

"""
Sends a welcome message to players
"""

from cuwo.script import ServerScript, ConnectionScript
from twisted.internet import reactor

class LoginNotice(ConnectionScript):
    def on_join(self, event):
        config = self.server.config.base
        welcome = self.server.format_lines(config.welcome)
        self.connection.send_lines(welcome)
        self.server.send_chat("%s has connected." % (self.connection.name))

    def on_unload(self):
        if not (self.connection.name is None):
            self.server.send_chat("%s has disconnected." % (self.connection.name)) 


class WelcomeServer(ServerScript):
    connection_class = LoginNotice


def get_class():
    return WelcomeServer
