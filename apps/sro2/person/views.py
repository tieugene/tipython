# -*- coding: utf-8 -*-
'''
Person views
----------
'''

from sro2.shared import *

@login_required
@render_to('sro2/person/person_list.html')
def    person_list(request, letter=''):
    '''
    Person list
    * get persons by first letter (ignor case:) )
    '''
    if not letter or letter=='a':
        letter=u'а'
    person_list = Person.objects.all().filter(Q(lastname__startswith=letter.capitalize())|Q(lastname__startswith=letter.lower())).order_by('lastname', 'firstname')
    return {'list': person_list, 'letter':letter}

@login_required
@render_to('sro2/person/person_view.html')
def    person_view(request, person_id):
    person    = Person.objects.get(pk=person_id)
    skill    = PersonSkill.objects.filter(person=person)
    orgstuff_list = person.orgstuff_set.all().order_by('org')
    return {
        'person': person,
        'person_skill': skill,
        'canedit': checkuser(person, request.user),
        'orgstuff_list': orgstuff_list,
    }

@login_required
def    person_del(request, person_id):
    item = Person.objects.get(pk=person_id)
    #log_it(request, item, DELETION)
    item.delete()
    return redirect(person_list,'а')

@login_required
@render_to('sro2/person/person_main.html')
def    person_main(request, person_id):
    person    = Person.objects.get(pk=person_id)
    skill    = PersonSkill.objects.filter(person=person)
    if request.method == 'POST':
        form = PersonMainForm(request.POST, instance=person)
        if form.is_valid():
            item = form.save()
            #log_it(request, item, ADDITION)
            return redirect(person_view,person_id=item.id)
    else:
        form = PersonMainForm(instance=person)
    return {'person': person, 'person_skill': skill, 'form': form }

@login_required
@render_to('sro2/person/person_skill.html')
def    person_skill(request, person_id):
    person = Person.objects.get(pk=person_id)
    if request.method == 'POST':
        form = PersonSkillForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.person = person
            item.save()
            #log_it(request, item, ADDITION)
            form = PersonSkillForm()
            add=True
    else:
        form = PersonSkillForm()
        add=False
    formdict = dict()
    formdict['person']        = person
    formdict['person_skill']    = PersonSkill.objects.filter(person=person)
    formdict['speciality']        = Speciality.objects.all()
    formdict['skill']        = Skill.objects.all()
    formdict['form']        = form
    formdict['form_speciality']    = PersonSkillAddSpecialityForm()
    formdict['form_skill']        = PersonSkillAddSkillForm()
    formdict['form_course']        = CourseForm()
    if add:
        return redirect(person_view,person_id=person_id)
    else:
        return formdict

@login_required
def    person_skill_add_speciality(request, person_id):
    if request.method == 'POST':
        form = PersonSkillAddSpecialityForm(request.POST)
        if form.is_valid():
            item = form.save()
            #log_it(request, item, ADDITION)
    return redirect(person_skill,person_id=person_id)

@login_required
def    person_skill_add_skill(request, person_id):
    if request.method == 'POST':
        form = PersonSkillAddSkillForm(request.POST)
        if form.is_valid():
            item = form.save()
            #log_it(request, item, ADDITION)
    return redirect(person_skill,person_id=person_id)

@login_required
def    person_skill_del(request, person_id, item_id):
    item = PersonSkill.objects.get(pk=item_id)
    #log_it(request, item, DELETION)
    item.delete()
    return redirect(person_view,person_id=person_id)

@login_required
@render_to('sro2/person/person_skill_edit.html')
def    person_skill_edit(request, person_id, item_id):
    person = Person.objects.get(pk=person_id)
    if request.method == 'POST':
        form = PersonSkillForm(request.POST)
        if form.is_valid():
            i = PersonSkill.objects.get(pk=item_id)
            courses=Course.objects.filter(personskill=i)
            item = form.save(commit=False)
            item.person = person
            item.save()
            item_id=item.id
            for c in courses:
                c.personskill=item
                c.save()
            i.delete()
            #log_it(request, item, ADDITION)
            form = PersonSkillForm()
            return redirect(person_view,person_id=person_id)
    else:
        form = PersonSkillForm()
    item = PersonSkill.objects.get(pk=item_id)
    formdict = dict()
    formdict['person']        = person
    formdict['person_skill']    = PersonSkill.objects.filter(person=person)
    formdict['speciality']        = Speciality.objects.all()
    formdict['skill']        = Skill.objects.all()

    form.initial={'speciality':item.speciality.id,'skill':item.skill.id,'year':item.year,'skilldate':item.skilldate,'school':item.school,'seniority':item.seniority,'seniodate':item.seniodate,'tested':item.tested}

    formdict['form']        = form
    formdict['form_speciality']    = PersonSkillAddSpecialityForm()
    formdict['form_skill']        = PersonSkillAddSkillForm()
    formdict['form_course']        = CourseForm()
    formdict['item'] = item
    return formdict

@login_required
def    person_course_add(request, person_id, item_id):
    '''
    Add course to speciality
    * parse submitted form
    '''
    item = PersonSkill.objects.get(pk=item_id)
    form = CourseForm(request.POST)
    if form.is_valid():
        course = form.save(commit=False)
        course.personskill=item
        course.save()
        #log_it(request, course, ADDITION)
    return redirect(person_skill_edit,person_id=person_id,item_id=item_id)

@login_required
def    person_course_del(request, person_id, item_id, course_id):
    '''
    Simple course deletation
    '''
    course = Course.objects.get(pk=course_id)
    #log_it(request, course, DELETION)
    course.delete()
    return redirect(person_skill_edit,person_id=person_id,item_id=item_id)

@login_required
def    person_getskill(request,person_id):
    '''
    Return person skill for ajax in add stuff
    '''
    return HttpResponse('%s' % (get_skill(person_id)))

def    get_skill(person_id):
    '''
    Get person skill function

    * format string from _all_ person skills with seniority and skill grade
    '''
    skill=''
    person = PersonSkill.objects.all().filter(person=person_id)
    if person.count>1:
        for item in person:
            if item.skill.high:
                skill_high=' (высшее)'
            else:
                skill_high=''
            skill='%s, %s (Стаж: %s), %s%s' % (skill,item.speciality.name,item.seniority,item.skill.name,skill_high)
        skill=skill[2:]
    else:
        skill='%s (Стаж: %s)' % (person.speciality.name,item.seniority)
    if not skill:
        skill='Специальность не указана.'
    return skill

