# -*- coding: utf-8 -*-

# 1. Flask
from flask import render_template, Response
# 2. My app
from __init__ import app
from forms import MyForm
# 3. 3rd parties
import trml2pdf
# 4. system
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def __tune_data(f):
    def __is_it(v, i):
        return 'X' if v == i else ''
    def __split_date(d):
        if (d):
            retvalue = '%02d' % d.day, '%02d' % d.month, '%04d' % d.year
        else:
            retvalue = '', '', ''
        return retvalue
    # selects:
    _m_gender    = bool(f.m_gender.data == u'1')
    _m_aim       = int(f.m_aim.data)
    _m_perm      = int(f.m_perm_type.data)
    _a_type      = bool(f.a_type.data == u'1')
    # dates:
    #m_arrived   = __date_split(f.m_arrived.data),
    d = dict(
        m_lastname      = f.m_lastname.data.upper(),
        m_firstname     = f.m_firstname.data.upper(),
        m_citizenship   = f.m_citizenship.data.upper(),
        m_gender        = ('X' if _m_gender else '','X' if not _m_gender else ''),
        m_aim           = (__is_it(_m_aim, 1),
                           __is_it(_m_aim, 2),
                           __is_it(_m_aim, 3),
                           __is_it(_m_aim, 4),
                           __is_it(_m_aim, 5),
                           __is_it(_m_aim, 6),
                           __is_it(_m_aim, 7),
                           __is_it(_m_aim, 8),
                           __is_it(_m_aim, 9)),
        m_profession    = f.m_profession.data.upper(),
        m_arrived       = __split_date(f.m_arrived.data),
        m_expired       = __split_date(f.m_expired.data),
        m_agent         = f.m_agent.data.upper(),       # TODO: split into 2 parts
        m_prev_addr     = f.m_prev_addr.data.upper(),   # TODO: split into 3 parts
        m_birth_date    = __split_date(f.m_birth_date.data),
        m_birth_country = f.m_birth_country.data.upper(),
        m_birth_city    = f.m_birth_city.data.upper(),
        m_doc_type      = f.m_doc_type.data.upper(),
        m_doc_series    = f.m_doc_series.data.upper(),
        m_doc_no        = f.m_doc_no.data.upper(),
        m_doc_date      = __split_date(f.m_doc_date.data),
        m_doc_expired   = __split_date(f.m_doc_expired.data),
        m_perm_type     = (__is_it(_m_perm, 1), __is_it(_m_perm, 2), __is_it(_m_perm, 3)),
        m_perm_series   = f.m_doc_series.data.upper(),
        m_perm_no       = f.m_doc_no.data.upper(),
        m_perm_date     = __split_date(f.m_doc_date.data),
        m_perm_expired  = __split_date(f.m_doc_expired.data),
        m_mk_series     = f.m_mk_series.data.upper(),
        m_mk_no         = f.m_mk_no.data.upper(),
        addr_sf         = f.addr_sf.data.upper(),
        addr_region     = f.addr_region.data.upper(),
        addr_city       = f.addr_city.data.upper(),
        addr_street     = f.addr_street.data.upper(),
        addr_house      = f.addr_house.data.upper(),
        addr_housing    = f.addr_housing.data.upper(),
        addr_building   = f.addr_building.data.upper(),
        addr_app        = f.addr_app.data.upper(),
        addr_tel        = f.addr_tel.data.upper(),
        a_type          = ('X' if _a_type else '','X' if not _a_type else ''),
        a_lastname      = f.a_lastname.data.upper(),
        a_firstname     = f.a_firstname.data.upper(),
        a_birth_date    = __split_date(f.a_birth_date.data),
        a_doc_type      = f.a_doc_type.data.upper(),
        a_doc_series    = f.a_doc_series.data.upper(),
        a_doc_no        = f.a_doc_no.data.upper(),
        a_doc_date      = __split_date(f.a_doc_date.data),
        a_doc_expired   = __split_date(f.a_doc_expired.data),
        a_addr_sf       = f.a_addr_sf.data.upper(),
        a_addr_region   = f.a_addr_region.data.upper(),
        a_addr_city     = f.a_addr_city.data.upper(),
        a_addr_street   = f.a_addr_street.data.upper(),
        a_addr_house    = f.a_addr_house.data.upper(),
        a_addr_housing  = f.a_addr_housing.data.upper(),
        a_addr_buildin  = f.a_addr_building.data.upper(),
        a_addr_app      = f.a_addr_app.data.upper(),
        a_addr_tel      = f.a_addr_tel.data.upper(),
        a_org_name      = f.a_org_name.data.upper(),
        a_org_addr      = f.a_org_addr.data.upper(),
        a_org_inn       = f.a_org_inn.data.upper(),
    )
    #print __date_split(f.m_arrived.data)
    #print m_arrived
    return d

@app.route('/', methods = ['GET', 'POST'])
def index():
    #form = MyForm(LANGUAGES=['ru',])
    form = MyForm()
    if form.validate_on_submit():
        # template (file.rml) + data (dict) | jinja (render_template) | trml2pdf(str): str | respose
        # retvalue = render_template
        # make_response
        # add content type
        # TODO: rml template as pre-loaded string
        # 1. prepare data
        #d = __tune_data(form)
        # 2. mk rml
        #rml = render_template('uvedomlenie.rml', d = d)  # str RML(str filename, dict dict)
        # 3. mk pdf
        #pdf = trml2pdf.parseString(rml) # str
        # 4. get out
        #rsp = Response(response=pdf, mimetype='application/pdf', content_type='application/pdf')
        #return rsp
        return Response(response=trml2pdf.parseString(render_template('uvedomlenie.rml', d = __tune_data(form))), mimetype='application/pdf', content_type='application/pdf')
    return render_template('index.html', form = form)
