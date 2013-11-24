# -*- coding: UTF-8 -*-
__author__ = 'ti.eugene@gmail.com'


from dasist import db
from datetime import datetime

class Contact(db.Model):
    id		= db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname	= db.Column(db.String(length=64))
    lastname	= db.Column(db.String(length=64))
    midname	= db.Column(db.String(length=64))
    birthdate	= db.Column(db.DateTime())

    def __unicode__(self):
        return '%s %s %s' % (self.lastname, self.firstname, self.midname)
