# -*- coding: utf-8 -*-


#from collections import defaultdict

from django import template
from django.contrib.contenttypes.models import ContentType

from apps.eav.views import eav_get_tags
from apps.eav.models import TaggedObject
from apps.eav.forms import TypeListForm

register = template.Library()

@register.filter
def    dquot(s):
    '''
    Return string w/ each quote doubled
    '''
    return s.replace('"', '""')

@register.filter_function
def    order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

# http://softwaremaniacs.org/blog/2009/09/21/trees-in-django-templates/
class TreeNode(template.Node):
    def __init__(self, tree, node_list):
        self.tree = tree
        self.node_list = node_list

    def render(self, context):
        tree = self.tree.resolve(context)

        # итератор по входному списку, выдающий пары вида (элемент списка, его подсписок), причём одного из элемента пары может не быть
        def pairs(items):

            # внутренний "грязный" генератор, выдающий пары, где могут быть бесполезные: с обоими пустыми head и tail
            def dirty(items):
                items = iter(items)
                head = None
                try:
                    while True:
                        item = items.next()
                        if isinstance(item, (list, tuple)):
                            yield head, item
                            head = None
                        else:
                            yield head, None
                            head = item
                except StopIteration:
                    yield head, None

            # фильтр над грязным генератором, удаляющий бесполезные пары
            return ((h, t) for h, t in dirty(items) if h or t)

        # выводит элемент списка с подсписком для подсписка рекурсивно вызывается render_items
        def render_item(item, sub_items, level):
            return ''.join([
                '<li>',
                item and self.node_list.render(template.Context({'item': item, 'level': level})) or '',
                sub_items and '<ul>%s</ul>' % ''.join(render_items(sub_items, level + 1)) or '',
                '</li>'
            ])

        # вывод списка элементов
        def render_items(items, level):
            return ''.join(render_item(h, t, level) for h, t in pairs(items))

        return render_items(tree, 0)

@register.tag
def tree(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError('"%s" takes one argument: tree-structured list' % bits[0])
    node_list = parser.parse('end' + bits[0])
    parser.delete_first_token()
    return TreeNode(parser.compile_filter(bits[1]), node_list)
"""
@register.filter
def astree(items, attribute):

    # перевод списка в dict: parent -> список детей
    parent_map = defaultdict(list)
    for item in items:
        parent_map[getattr(item, attribute)].append(item)

    # рекурсивный вывод детей одного parent'а
    def tree_level(parent):
        for item in parent_map[parent]:
            yield item
            sub_items = list(tree_level(item.id))
            if sub_items:
                yield sub_items
    return list(tree_level(None))
"""
@register.inclusion_tag('gw/tagged/taglist.html', takes_context=True)
def taglist(context,obj):
    try:
        to=TaggedObject.objects.get(object=obj)
        tags=eav_get_tags(to)
        return {'tags': tags,'item':obj,'context':context}
    except:
        ttypes=TypeListForm()
        return {'ttypes': ttypes,'item':obj,'context':context}

@register.filter
def    get_obj(type,id):
    try:
        ctype=ContentType.objects.get(id=type)
    except:
        ctype=ContentType.objects.get(id=type,app_label='gw')
    try:
        model=ctype.model_class()
        obj=model.objects.get(pk=int(id))
    except:
        obj=''
    return  obj

@register.filter
def    get_obj_link(type,id):
    try:
        ctype=ContentType.objects.get(id=type)
    except:
        ctype=ContentType.objects.get(id=type,app_label='gw')
    try:
        model=ctype.model_class()
        obj=model.objects.get(pk=int(id))
        if 'get_absolute_url' in dir(obj):
            link='<a href="%s" target="_blank">%s</a>' % (obj.get_absolute_url(),obj)
        else:
            link=obj
    except:
        link='Объект не существует.'
    return  link

@register.inclusion_tag('gw/file/attach.html')
def attachfile(obj):
    return {'item':obj}

