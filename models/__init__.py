# -*- coding: utf-8 -*-
'''
    Copyright [2012] [Redacted Labs]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''

from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer
from sqlalchemy.orm import sessionmaker
from models.BaseGameObject import BaseObject
from libs.ConfigManager import ConfigManager

metadata = BaseObject.metadata

config = ConfigManager.Instance()
db_connection = 'mysql://%s:%s@%s/%s' % (
    config.db_user, config.db_password, config.db_server, config.db_name)

# set the connection string here
engine = create_engine(db_connection)

Session = sessionmaker(bind=engine, autocommit=True)
dbsession = Session(autoflush=True)

association_table = Table('user_to_box', BaseObject.metadata,
                          Column('user_id',
                                 Integer, ForeignKey('user.id'), nullable=False),
                          Column('box_id',
                                 Integer, ForeignKey('box.id'), nullable=False)
                          )

# import models
from models.Box import Box
from models.PasteBin import PasteBin
from models.Permission import Permission
from models.Team import Team
from models.User import User
from models.FileUpload import FileUpload
from models.WallOfSheep import WallOfSheep

# calling this will create the tables at the database
__create__ = lambda: (
    setattr(engine, 'echo', True), metadata.create_all(engine))

# Bootstrap the database with some shit
def __boot_strap__():
    import setup.bootstrap
