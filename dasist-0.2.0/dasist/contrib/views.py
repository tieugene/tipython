# 2. 3rd parties
from dal import autocomplete
# 3. djangon
from django.shortcuts import render
from django.views.generic import DetailView, ListView
# 4. local
from . import models

PAGE_SIZE = 25

class OrgList(ListView):
    model = models.Org
    template_name = 'core/org_list.html'
    paginate_by = PAGE_SIZE


class OrgDetail(DetailView):
    model = models.Org
    template_name = 'core/org_detail.html'


def org_edit(request, pk):
    org = models.Org.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = forms.OrgEditForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            return redirect('org_view', org.pk)
    else:
        form = forms.OrgEditForm(instance=org)
#    return render_to_response('core/org_form.html', context_instance=RequestContext(request, {
#        'form': form,
#        'object': org,
#    }))
    return render(request, 'core/org_form.html', {
        'form': form,
        'object': org,
    })


def org_get_by_inn(request):
    """
    @param ?inn:str - INN
    @return: {'name': name, 'fullname': fullname}
    """
    inn = request.GET.get('inn')
    org = models.Org.objects.filter(inn=inn).first()
    if org:
        ret = dict(name=org.name, fullname=org.fullname)
    else:
        ret = None
    return HttpResponse(json.dumps(ret), content_type='application/json')


class OrgAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.Org.objects.none()
        qs = models.Org.objects.all()
        if self.q:
            if self.q.isdigit():
                qs = qs.filter(inn__istartswith=self.q)
            else:
                qs = qs.filter(name__istartswith=self.q)
        return qs
