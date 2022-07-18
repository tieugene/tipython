#!/bin/env python
# -*- coding: utf-8 -*-
'''
Test of static class variables.
What to test:
* Base:
1. BaseResource child wide vars - 1 time?
2. BaseRC wide vars from parent
* My:

'''
import os, sys, pprint, logging

reload(sys)
sys.setdefaultencoding('utf-8')

class	BaseResource:
	resvar = None

	def	__init__(self):
		pass

	def	get_childvar(self):
		return self.childvar

	def	set_childvar(self, var):
		self.childvar = var

class	BaseMember(BaseResource):
	childvar = 1

class	BaseCollection(BaseResource):
	childvar = 2

	def	get_mem(self):
		return BaseMember()

	def	get_col(self):
		return BaseCollection()

class	BaseRoot(BaseCollection):

	def	__init__(self):
		pass

	def	set_childvar_root(self, v):
		self.childvar = v

# ========

class	MyResource(BaseResource):
    @staticmethod
    def iscollection():
        return True

# ====

def	main():
    print MyResource().iscollection()
    br = BaseRoot()
    bc = br.get_col()
    bm1 = br.get_mem()
    bm2 = br.get_mem()
    # lets go
    print br.resvar
    print bc.childvar
    print bm1.childvar
    print bc.get_childvar()
    bm2.childvar = 11
    print bm1.childvar, bm1.get_childvar()
    print bm2.childvar, bm2.get_childvar()

if (__name__ == '__main__'):
	main()
