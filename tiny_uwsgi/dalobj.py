#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from gluon import DAL, Field
except:
    raise Exception('web2py.gluon not found')


class DalObj(object):

    def __init__(self, daldb, objname, objdef):
        self.db = daldb
        self.objname = objname

        self.db.define_table(
            objname,
            *[self.makeField(fa) for fa in objdef]
        )

    def makeIndex(self, fielddef):
        try:
            for f in fielddef:
                IndexName = 'index_{tablename}_{fieldname}'.format(
                    tablename=self.objname, fieldname=f)

                query = 'CREATE INDEX {idxname} ON {tablename} ({fieldname});'.format(
                    idxname=IndexName, tablename=self.objname, fieldname=f)
                try:
                    self.db.executesql(query)
                    print query
                except:
                    print 'already exist {idxname}'.format(idxname=IndexName)

        except TypeError:
            print 'error makeIndex', fielddef

    def removeIndex(self, fielddef):
        try:
            for f in fielddef:
                IndexName = 'index_{tablename}_{fieldname}'.format(
                    tablename=self.objname, fieldname=f)

                query = 'DROP INDEX {idxname} on {tablename};'.format(
                    idxname=IndexName, tablename=self.objname)
                try:
                    self.db.executesql(query)
                    print query
                except:
                    print 'not exist {idxname}'.format(idxname=IndexName)

        except TypeError:
            print 'error removeIndex', fielddef

    def makeField(self, fa):
        return Field(fa[0], fa[1], **fa[2])

    def truncate(self):
        self.db[self.objname].truncate()


class DBDataMixinBase(object):

    def __init__(self, dbconn):
        self.db = DAL(**dbconn)
        self.dalobjs = {}

    def loadAllTables(self, objdefs):
        for vs in objdefs:
            self.dalobjs[vs[0]] = DalObj(self.db, vs[0], vs[1:])

    def loadSomeTables(self, objdefs, tablelist):
        for vs in objdefs:
            if vs[0] in tablelist:
                self.dalobjs[vs[0]] = DalObj(self.db, vs[0], vs[1:])

    def makeIndex(self, indexDef):
        for k, v in indexDef.iteritems():
            self.dalobjs[k].makeIndex(indexDef[k])

    def removeIndex(self, indexDef):
        for k, v in indexDef.iteritems():
            self.dalobjs[k].removeIndex(indexDef[k])

    def truncateTables(self, tablelist):
        for tn in tablelist:
            self.dalobjs[tn].truncate()

    def closeDB(self):
        self.db.close()

if __name__ == "__main__":
    dbconn = dict(
        uri="sqlite:memory",
    )

    ObjDefs = (
        ('userinfo',
         ('username', 'string', dict(length=255, notnull=True)),
         ('email', 'string', dict(length=255, notnull=True)),
         ('phone', 'string', dict(length=255, notnull=True)),
         ('joindate', 'datetime', dict(notnull=True))
         ),
    )
    dbobj = DBDataMixinBase(dbconn)
    dbobj.loadAllTables(ObjDefs)
    IndexDef = {
        'userinfo': ('username', 'email'),
    }
    dbobj.makeIndex(IndexDef)
