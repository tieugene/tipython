# -*- coding: utf-8 -*-
'''
SRO2 URLs
'''
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib.auth.views import login, logout
#import django.views.generic
from models import *
###(1
from gw.models import *
###1)

#for m in modellist:
#    databrowse.site.register(m)

urlpatterns = patterns('sro2.views',
# Index
    (r'^$',                                                                                             'index'),
    (r'^about/$',                                                                                       'about'),

# Journal
    (r'^journal/$',                                                                                     'journal_ng'),
    (r'^journal/(?P<ctype>(.*))/(?P<obj_id>\d+)/$',                                                     'journal_ng_obj'),
    (r'^journal/(?P<start_date>(.*))/(?P<end_date>(.*))/$',                                             'journal_ng'),

# Orglist
    (r'^orglist/(?P<sro_id>\d+)/get_list/$',                                                            'orglist_list_get'),
    (r'^orglist/(?P<sro_id>\d+)/list/(?:(?P<page_num>\d+)/)?$',                                         'orglist_list'),
    (r'^orglist/(?P<sro_id>\d+)/publish/$',                                                             'orglist_publish'),
    (r'^orglist/(?P<sro_id>\d+)/publish/member/(?P<item_id>\d+).html$',                                 'orglist_publish_member'),
    (r'^orglist/(?P<sro_id>\d+)/publish/permit/(?P<item_id>\d+).html$',                                 'orglist_publish_permit'),
    (r'^orglist/(?P<sro_id>\d+)/upload/$',                                                              'orglist_upload'),
    (r'^orglist/(?P<sro_id>\d+)/table/$',                                                               'orglist_table'),
    (r'^orglist/(?P<sro_id>\d+)/csv/$',                                                                 'orglist_csv'),
    (r'^orglist/(?P<sro_id>\d+)/rtnu/$',                                                                'orglist_rtnu'),
    (r'^orglist/(?P<sro_id>\d+)/rtne/$',                                                                'orglist_rtne'),
    (r'^orglist/(?P<sro_id>\d+)/rtnh/$',                                                                'orglist_rtnh'),
    (r'^orglist/(?P<sro_id>\d+)/add/$',                                                                 'orglist_org_add'),
    (r'^orglist/(?P<sro_id>\d+)/addexists/$',                                                           'orglist_org_add_exists'),
    (r'^orglist/(?P<sro_id>\d+)/find/$',                                                                'orglist_find'),
    (r'^orglist/mail_sel/(?P<orgs>(.*))/$',                                                             'orglist_mail_sel'),
    (r'^orglist/print/envelope/(?P<orgs>(.*))/$',                                                       'orglist_print_envelope'),
    (r'^orglist/print/notification/(?P<orgs>(.*))/$',                                                   'orglist_print_notification'),
    (r'^orglist/print/maillist/(?P<orgs>(.*))/$',                                                       'orglist_print_maillist'),

# Organisation
    (r'^orgsro/(?P<orgsro_id>\d+)/$',                                                                   'orgsro_view'),
    (r'^orgsro/(?P<sro_id>\d+)/(?P<org_id>\d+)/$',                                                      'orgsro_view'),
    (r'^orgsro/(?P<orgsro_id>\d+)/del/$',                                                               'orgsro_del'),
    (r'^orgsro/(?P<orgsro_id>\d+)/org/$',                                                               'orgsro_org_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/main/$',                                                              'orgsro_main_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/okved/edit/$',                                                        'orgsro_okved_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/okved/(?P<item_id>\d+)/del/$',                                        'orgsro_okved_del'),
    #(r'^orgsro/(?P<orgsro_id>\d+)/phone/edit/$',                                                        'orgsro_phone_edit'),
    #(r'^orgsro/(?P<orgsro_id>\d+)/phone/(?P<item_id>\d+)/del/$',                                        'orgsro_phone_del'),
    #(r'^orgsro/(?P<orgsro_id>\d+)/email/edit/$',                                                        'orgsro_email_edit'),
    #(r'^orgsro/(?P<orgsro_id>\d+)/email/(?P<item_id>\d+)/del/$',                                        'orgsro_email_del'),
    #(r'^orgsro/(?P<orgsro_id>\d+)/www/edit/$',                                                          'orgsro_www_edit'),
    #(r'^orgsro/(?P<orgsro_id>\d+)/www/(?P<item_id>\d+)/del/$',                                          'orgsro_www_del'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/edit/$',                                                        'orgsro_stuff_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/table/$',                                                       'orgsro_stuff_table'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/add_person/$',                                                  'orgsro_stuff_add_person'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/(?P<item_id>\d+)/add_exist/$',                                  'orgsro_stuff_add_exist'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/add_role/$',                                                    'orgsro_stuff_add_role'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/(?P<item_id>\d+)/del/$',                                        'orgsro_stuff_del'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/(?P<item_id>\d+)/return/$',                                     'orgsro_stuff_return'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/(?P<item_id>\d+)/dismiss/(?P<enddate>[^//]*)$',                 'orgsro_stuff_dismiss'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/(?P<orgstuff_id>\d+)/edit/$',                                   'orgsro_stuff_orgstuff_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/stuff/add/$',                                                         'orgsro_stuff_orgstuff_add'),
    (r'^orgsro/(?P<orgsro_id>\d+)/cetrificate/$',                                                       'orgsro_certificate'),
    (r'^orgsro/(?P<orgsro_id>\d+)/extract/(?P<full>\d+)/$',                                             'orgsro_extract'),
    (r'^orgsro/(?P<orgsro_id>\d+)/license/add/$',                                                       'orgsro_license_add'),
    (r'^orgsro/(?P<orgsro_id>\d+)/license/edit/$',                                                      'orgsro_license_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/license/del/$',                                                       'orgsro_license_del'),
    (r'^orgsro/(?P<orgsro_id>\d+)/insurance/add/$',                                                     'orgsro_insurance_add'),
    (r'^orgsro/(?P<orgsro_id>\d+)/insurance/edit/$',                                                    'orgsro_insurance_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/insurance/del/$',                                                     'orgsro_insurance_del'),
    (r'^orgsro/(?P<orgsro_id>\d+)/event/edit/$',                                                        'orgsro_event_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/event/(?P<item_id>\d+)/del/$',                                        'orgsro_event_del'),
    (r'^orgsro/(?P<orgsro_id>\d+)/specedit/$',                                                          'orgsro_spec_edit'),
    (r'^orgsro/(?P<orgsro_id>\d+)/specdel/$',                                                           'orgsro_spec_del'),
    (r'^orgsro/(?P<orgsro_id>\d+)/to_member/$',                                                         'orgsro_to_member'),
    (r'^orgsro/(?P<orgsro_id>\d+)/to_candidate/$',                                                      'orgsro_to_candidate'),
    (r'^orgsro/(?P<orgsro_id>\d+)/to_archive/$',                                                        'orgsro_to_archive'),
    (r'^orgsro/(?P<orgsro_id>\d+)/to_excluded/$',                                                       'orgsro_to_excluded'),
    (r'^orgsro/(?P<orgsro_id>\d+)/return_member/$',                                                     'orgsro_return_member'),
    (r'^orgsro/(?P<orgsro_id>\d+)/edit/$',                                                              'orgsro_stagelist_edit'),
    (r'^org/(?P<org_id>\d+)/$',                                                                         'org_view'),

# Person
    (r'^person/list/(?P<letter>.*)$',                                                                   'person_list'),
    (r'^person/(?P<person_id>\d+)/getskill/$',                                                          'person_getskill'),
    (r'^person/(?P<person_id>\d+)/del/$',                                                               'person_del'),
    (r'^person/(?P<person_id>\d+)/$',                                                                   'person_view'),
    (r'^person/(?P<person_id>\d+)/main/$',                                                              'person_main'),
    (r'^person/(?P<person_id>\d+)/skill/$',                                                             'person_skill'),
    (r'^person/(?P<person_id>\d+)/skill/add_speciality/$',                                              'person_skill_add_speciality'),
    (r'^person/(?P<person_id>\d+)/skill/add_skill/$',                                                   'person_skill_add_skill'),
    (r'^person/(?P<person_id>\d+)/skill/(?P<item_id>\d+)/del/$',                                        'person_skill_del'),
    (r'^person/(?P<person_id>\d+)/skill/(?P<item_id>\d+)/edit/$',                                       'person_skill_edit'),
    (r'^person/(?P<person_id>\d+)/skill/(?P<item_id>\d+)/edit/course_add$',                             'person_course_add'),
    (r'^person/(?P<person_id>\d+)/skill/(?P<item_id>\d+)/edit/course_del/(?P<course_id>\d+)$',          'person_course_del'),

# Stagelist
    (r'^stagelist/(?P<stagelist_id>\d+)/editstages/$',                                                  'stagelist_editstages'),
    (r'^stagelist/(?P<stagelist_id>\d+)/html/$',                                                        'stagelist_html'),
    (r'^stagelist/(?P<stagelist_id>\d+)/dup/$',                                                         'stagelist_dup'),
    (r'^stagelist/(?P<stagelist_id>\d+)/cmp/$',                                                         'stagelist_cmp'),
    (r'^stagelist/(?P<stagelist_id>\d+)/compare/$',                                                     'stagelist_compare'),
    (r'^stagelist/(?P<stagelist_id>\d+)/cmp/(?P<dest_id>\d+)$',                                         'stagelist_cmp_ajax'),
    (r'^stagelist/(?P<stagelist_id>\d+)/(?P<full>\d+)/(?P<danger>\d+)/$',                               'stagelist_view'),
    (r'^stagelist/(?P<stagelist_id>\d+)/edit/$',                                                        'stagelist_edit'),

# Statement
    (r'^statement/(?P<orgsro_id>\d+)/add/$',                                                            'statement_add'),
    (r'^statement/(?P<statement_id>\d+)/dup/$',                                                         'statement_dup'),
    (r'^statement/(?P<statement_id>\d+)/attachment_pdf/$',                                              'statement_attachment_pdf'),
    (r'^statement/(?P<statement_id>\d+)/del/$',                                                         'statement_del'),
    (r'^statement/(?P<statement_id>\d+)/(?P<full>\d+)/(?P<danger>\d+)/$',                               'statement_view'),
    (r'^statement/(?P<statement_id>\d+)/edit/$',                                                        'statement_edit'),
    (r'^statement/(?P<statement_id>\d+)/link/(?P<permit_id>\d+)$',                                      'statement_link'),

# Permit
    (r'^permit/(?P<orgsro_id>\d+)/add/$',                                                               'permit_add'),
    (r'^permit/(?P<permit_id>\d+)/pdf/$',                                                               'permit_pdf'),
    (r'^permit/(?P<permit_id>\d+)/dup/$',                                                               'permit_dup'),
    (r'^permit/(?P<permit_id>\d+)/pause_allstages/$',                                                   'permit_pause_allstages'),
    (r'^permit/(?P<permit_id>\d+)/resume_allstages/$',                                                  'permit_resume_allstages'),
    (r'^permit/(?P<permit_id>\d+)/del/$',                                                               'permit_del'),
    (r'^permit/(?P<permit_id>\d+)/setdefault/$',                                                        'permit_setdefault'),
    (r'^permit/(?P<orgsro_id>\d+)/resetdefault/$',                                                      'permit_resetdefault'),
    (r'^permit/(?P<permit_id>\d+)/(?P<full>\d+)/(?P<danger>\d+)/$',                                     'permit_view'),
    (r'^permit/(?P<permit_id>\d+)/edit/$',                                                              'permit_edit'),
    (r'^permit/(?P<permit_id>\d+)/history/$',                                                           'permit_history'),
    (r'^permit/(?P<permit_id>\d+)/rollback/(?P<dest_id>\d+)$',                                          'permit_rollback'),

# Alien permit
    (r'^alienpermit/(?P<orgsro_id>\d+)/add/$',                                                          'alienpermit_add'),

# Protocol
    (r'^protocol/(?P<sro_id>\d+)/list/$',                                                               'protocol_list'),
    (r'^protocol/(?P<sro_id>\d+)/add/$',                                                                'protocol_add'),
    (r'^protocol/(?P<protocol_id>\d+)/$',                                                               'protocol_view'),
    (r'^protocol/(?P<protocol_id>\d+)/main/$',                                                          'protocol_main'),
    (r'^protocol/(?P<protocol_id>\d+)/del/$',                                                           'protocol_del'),
    (r'^protocol/(?P<protocol_id>\d+)/rtn/$',                                                           'protocol_rtn'),
    (r'^protocol/(?P<protocol_id>\d+)/report/$',                                                        'protocol_report'),

# Report
    (r'^report/$',                                                                                      'report'),
    (r'^report/branches/$',                                                                             'report_branches_orglist'),
    (r'^report/speclist/$',                                                                             'report_speclist'),
    (r'^report/byuser/$',                                                                               'report_byuser_list'),
    (r'^report/statements/$',                                                                           'report_statements_list'),
    (r'^report/orgcount/$',                                                                             'report_orgcount'),
    (r'^report/permit/$',                                                                               'report_permit'),
    (r'^report/subject/$',                                                                              'report_subject'),

# Sro
    (r'^sro/list$',                                                                                     'sro_list'),
    (r'^sro/new$',                                                                                      'sro_new'),
    (r'^sro/edit/(?P<sro_id>\d+)$',                                                                     'sro_edit'),
    (r'^sro/view/(?P<sro_id>\d+)$',                                                                     'sro_view'),
    (r'^sro/del/(?P<sro_id>\d+)$',                                                                      'sro_del'),

# Dev
    (r'^unilist/(?P<obj>[^//]*)/(?P<critline>[^//]*)$',                                                 'unilist'),
    (r'^benchmark$',                                                                                    'benchmark'),
#    (r'^log/$',                                                                                    'test'),
    #(r'^log/(?P<start_date>(.*))/(?P<end_date>(.*))/$',                                             'journal_ng'),



#    (r'^migrate/$',                                                                                     'migrate_course_year'),
#    (r'^clrps/$',                                                                                       'clear_persons'),
#    (r'^models2gw/$',                                                                                   'models2gw'),
    
#    (r'^permit/(?P<permit_id>\d+)/pause/(?P<danger>\d+)/$',                                            'permit_pause'),
#    (r'^stagelist/(?P<stagelist_id>\d+)/pausestages/(?P<danger>\d+)$',                                 'stagelist_pausestages'),
)
