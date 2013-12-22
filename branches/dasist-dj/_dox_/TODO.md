+1. CRUD Bill (w/o m2ms)
2. Add Route to Bill (as m2m):
-- views:
--- C
--- U
-- forms: тут есть варианты
* as is (formset) + JS + formset validate
* builtin (generic/Base...)
* orderedm2m
* partially built-in (CheckBoxMultiple - like a "solo")
* pure hack (hidden cherfiled + OLs + buttons + JS)
-- tpl:
--- ...
3. Route Bills
4. Filter by Role
5. ACL by Role
6. Add comments

Feature:
1. Project and Depart as models (?)
2. mailto
3. thunderbird-lightning.Tasks

Tuning:
* State
* Перезапустить несогласованный
* webp
* перехват соглашенных счетов
* check "already exists"
* form: up/down

<li> <select name="form-{{forloop.counter0}}-approve" id="id_form-{{forloop.counter0}}-approve"> <option value="{{form.approve.pk}}" selected="selected"> {{ form.approve.in }} </option> </select> </li>
<li>
	<select name="form-{{forloop.counter0}}-approve" id="id_form-{{forloop.counter0}}-approve">
		<option value="{{form.approve.pk}}" selected="selected">
			{{ form.approve.label_from_instance }}
		</option>
	</select>
</li>
