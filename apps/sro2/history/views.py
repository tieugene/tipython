# -*- coding: utf-8 -*-
'''
History views
-------------
'''
from sro2.shared import *

class History(object):
    '''
    History container-class
    '''
    def __init__(self,orgsro):
        self.orgsro=orgsro
        self.p=orgsro.currperm


    def originals(self):
        '''
        Return only original permits (without snapshots)
        '''
        originals=Permit.objects.filter(status=0,orgsro=self.orgsro).order_by('date')

        return originals

    def snaps_of(self,permit):
        '''
        Return all snapshots of permit
        '''
        snaps=Permit.objects.filter(status__gt=0,orgsro=self.orgsro,no=permit.no)
        return snaps

    def last_snap(self,permit):
        snaps=self.snaps_of(permit).order_by('id')
        if snaps:
            last = snaps.reverse()[0]
            return last
        else:
            return permit


    def prevs(self):
        '''
        Return previous permits
        '''
        orig=self.originals()
        if self.orgsro.currperm and self.orgsro.currperm.date:
            return orig.exclude(id=self.orgsro.currperm.id).exclude(date__gt=self.orgsro.currperm.date)
        else:
            return orig

    def is_full(self,ch):
        '''
        Return True if this snapshot is Full Pause or Full Resume.

        # If you already have results of __cmp_stagelists do ch.common=common - it make function _really_ faster.
        '''
        tl=0
        for t in PermitStage.objects.filter(stagelist=self.p):
            if not t.stage.isgroup:
                tl+=1
        l=0
        ch.paused=False
        if not hasattr(ch,'common'):
            hist=self.orgsro.stagelist_set.filter(permit__no=ch.no).order_by('permit__date') # get snapshots of permit
            n=0
            for st in hist:
                if st!=ch:
                    n+=1
                else:
                    deleted, added, common = self.cmp_stagelists(hist[n-1],ch) # diff between snaps
                    ch.common=common
        for c in ch.common:
            if c.paused!=c.newdate and not c.stage.isgroup:
                l+=1 # count of changes for full pausing/resuming
                if c.newdate is not None and not ch.paused:
                    ch.paused=True
        if tl==l:
            return True
        else:
            return False
    def    get_history(self):
        '''
        Get permits history

        # TODO: make correct names of dates (date,datesince,datedue,datetill and others)

        # go to docs/history.rst for explanation of history system

        @OrgSro orgsro

        < dict:
            * str:desc -- formatted string to insert in reports
            * Protocol:protocol -- protocol of this change
            * int:durance -- days - pause range
            * Date:date -- date of change
            * Date:datesince -- f**k, im missing in this dates=((

        '''
        history=[]
        p=self.orgsro.currperm # get current permit.
        if p:
            hist=self.orgsro.stagelist_set.filter(permit__no=p.no).order_by('permit__date') # get snapshots of permit
            n=1
            for ch in hist:
                if ch!=p and n<(len(hist)):
                    deleted, added, common = self.cmp_stagelists(hist[n-1],ch) # diff between snaps
                    ch.common=common
                    n+=1
                    for c in common:
                        if c.newdate:
                            dur=c.newdate-ch.date
                            ch.datesince=c.newdate # get datesince for history entity
                            break
                    if self.is_full(ch): # if permit fully changed
                        if ch.paused: #pause case
                            h={'desc':'<b>Свидетельство №%s от %s (%s) - Действующее:</b><br> Действие Свидетельства приостановлено с %s по %s в отношении всех видов работ в соответствии со статьей 55.5 ГрК РФ на основании решения Дисциплинарной комиссии, %s, на срок %s календарный дней.' %
                                    (p.no,self.__strdatedot(p.date),p.protocol.asstr_full(),self.__strdatedot(ch.date),self.__strdatedot(ch.datesince),ch.protocol.asstr_full(),dur.days),'protocol':ch.protocol,'durance':dur.days,'date':ch.date,'datesince':ch.datesince}
                            history.append(h)
                        else: # resume case
                            h={'desc':'<b>Свидетельство №%s от %s (%s) - Действующее:</b><br> Действие Свидетельства возобновлено с %s в отношении всех видов работ на основании решения Дисциплинарной комиссии, %s.' % (p.no,self.__strdatedot(p.date),p.protocol,self.__strdatedot(ch.date),ch.protocol.asstr_full(),),'protocol':ch.protocol,'date':ch.date}
                            history.append(h)
            return history
        else:
            return False

    def    __strdatedot(self,date):
        if date:
            date = str(date).split('-')
            date ='%s.%s.%s' % (date[2], date[1], date[0])
            return date
        else:
            return ''


    def    cmp_stagelists(self,src, dst, group=False):
        '''
        Compare 2 stagelists.

        @param s:StageList - source

        @param d:StageList - destination

        @param group:     True: group of stages is included to result only if all substages've been included to result (for deleted and added)

        @        False: group of stages is included to result if at least one of substages's been included to result (for deleted and added)

        @return Stage:
            * PermitStage: deleted
            * PermitStage: added
            * PermitStage: common (annotated w/ newdate)

        '''
        v_src_o = set(src.permitstage_set.filter(danger=False).values_list('stage', flat=True))
        v_dst_o = set(dst.permitstage_set.filter(danger=False).values_list('stage', flat=True))
        v_del_o = v_src_o - v_dst_o
        v_add_o = v_dst_o - v_src_o
        v_both_o = v_src_o & v_dst_o
        v_src_d = set(src.permitstage_set.filter(danger=True).values_list('stage', flat=True))
        v_dst_d = set(dst.permitstage_set.filter(danger=True).values_list('stage', flat=True))
        v_del_d = v_src_d - v_dst_d
        v_add_d = v_dst_d - v_src_d
        v_both_d = v_src_d & v_dst_d

        deleted = src.permitstage_set.filter(danger=False, stage__in=v_del_o) | src.permitstage_set.filter(danger=True, stage__in=v_del_d)
        added = dst.permitstage_set.filter(danger=False, stage__in=v_add_o) | dst.permitstage_set.filter(danger=True, stage__in=v_add_d)

        if group:
            for permitstage in deleted.filter(stage__isgroup=True):
                permitstage_list = deleted.filter(danger=permitstage.danger, stage__parent=permitstage.stage)
                if permitstage.danger:
                    stage_list = Stage.objects.filter(parent=permitstage.stage)
                else:
                    stage_list = Stage.objects.filter(parent=permitstage.stage, dangeronly=False)
                if permitstage_list.count() != stage_list.count():
                    deleted = deleted.exclude(id=permitstage.id)

            for permitstage in added.filter(stage__isgroup=True):
                permitstage_list = added.filter(danger=permitstage.danger, stage__parent=permitstage.stage)
                if permitstage.danger:
                    stage_list = Stage.objects.filter(parent=permitstage.stage)
                else:
                    stage_list = Stage.objects.filter(parent=permitstage.stage, dangeronly=False)
                if permitstage_list.count() != stage_list.count():
                    added = added.exclude(id=permitstage.id)
        return (
            deleted,
            added,
            (src.permitstage_set.filter(danger=False, stage__in=v_both_o) | src.permitstage_set.filter(danger=True, stage__in=v_both_d)).extra(select={'newdate': 'SELECT paused FROM sro2_permitstage AS other WHERE other.stagelist_id = %s AND other.stage_id = sro2_permitstage.stage_id AND other.danger = sro2_permitstage.danger' % dst.pk})
        )

    def    permits2str(self, sep=u'\n'):
        '''
        @return str: string of permits
        '''
        #p=self.orgsro.currperm
        line=''
        self.history=self.get_history()
        if self.p and self.p.protocol:
            if self.orgsro.status==2:
                if self.history:
                    line+=self.history[-1]['desc'].replace('<b>','').replace('</b>','').replace('<br>','\n')+'\n'
                else:
                    line+=u'Свидетельство №%s от %s (%s) - Действующее:\n' % (self.p.no,self.__strdatedot(self.p.date),self.p.protocol.asstr_full())
            else:
                reasons=''
                for orgreason in self.orgsro.orgreason_set.all():
                    if reasons:
                        reasons+=', '+orgreason.reason.title
                    else:
                        reasons=orgreason.reason.title
                try:
                    line+='Членство от %s прекращено на основании %s. %s\n' % (strdatedot(self.orgsro.escludedate),reasons,self.orgsro.exprotocol.asstr_full())
                except:
                    line+='Членство прекращено некорректно'
                line+=u'Свидетельство №%s от %s (%s) - аннулировано в связи с прекращением членства.\n' % (self.p.no,self.__strdatedot(self.p.date),self.p.protocol.asstr_full())
            line+=u'Перечень видов работ, которые оказывают влияние на безопасность объектов капитального строительства:'
            line+= self._csv_stages(self.p, False)
            if self.p.permitstage_set.count_danger():
                line +=(u'\nПеречень видов работ, которые оказывют влияние на безопасность особо опасных, технически сложных и уникальных объектов:\n')
            line += self._csv_stages(self.p, True)
        else:
            line+='Организация не имеет действующих свидетельств.'
        return line


    def    _csv_stages(self,stagelist, danger, sep=u'\n'):
        q = stagelist.permitstage_set.filter(danger=danger).order_by('stage__id',).values_list('stage__ver', 'stage__parent', 'stage__code', 'stage__name')
        subitems = list()
        field = u''
        for i in q:
            if (i[1]):
                subitems.append(i[2])
            else:
                if (subitems):
                    field += (sep + ', '.join(subitems))
                    subitems = list()
                field += (sep + i[2] + '. ' + i[3])
        if (subitems):
            field += (sep + ', '.join(subitems))
            subitems = list()
        return field
