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
PvP Leaderboard for Cuwo by Nastus
"""

from cuwo.script import ServerScript, ConnectionScript
import MySQLdb as mdb

host = 'hostname'
passw = 'password'
user = 'username'
db = 'database'

class DbHandler(ConnectionScript):
        
    def on_kill(self, event):
        self.pl_exists(event.target.name)
        self.cur = self.open_con().cursor()
        self.cur.execute("UPDATE kill_keeper SET kill_count = kill_count+1 WHERE player = %s",(self.connection.name))
        self.cur.execute("UPDATE kill_keeper SET death_count = death_count+1 WHERE player = %s",(event.target.name))
        self.close_con()
        
    def open_con(self):
        try:
            self.con = mdb.connect(host,user,passw,db);
            return self.con
        except mdb.Error, e:
            print "Could not connect to the database, Error %d: %s" % (e.args[0], e.args[1])
        
    def close_con(self):
        if self.con:
            self.con.close()
    
    def pl_exists(self, enemy):
        self.cur = self.open_con().cursor()
        if enemy is not None:
            self.cur.execute("SELECT * FROM kill_keeper WHERE player = %s",(enemy))
            if self.cur.rowcount == 0:
                self.cur.execute("INSERT INTO kill_keeper(player,kill_count,death_count) VALUES(%s,'0','0')",(enemy))
                
        self.cur.execute("SELECT * FROM kill_keeper WHERE player = %s",(self.connection.name))
        if self.cur.rowcount == 0:
            self.cur.execute("INSERT INTO kill_keeper(player,kill_count,death_count) VALUES(%s,'0','0')",(self.connection.name))
        self.close_con()

class DbHandle(ServerScript):
    connection_class = DbHandler
    
    def on_load(self):
        print "Started PvP Leaderboard"
        
def get_class():
    return DbHandle