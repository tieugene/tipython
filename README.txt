= Structures =

== Inner ==

=== now ===

{ field_name: field_value (natural python type), }

=== will ===

...

== DB ==

Doc:
	name:str
	data:json=>dict	# w/o 'name'; dicts can be nested (1 level)

== form ==
{
	'form': forms.Form
	'formsets': SortedDict(formset:FormSet)[]
}
== out ==

(read/print/preview) - similar to inner/Doc
{
	'data': { field_label: field_value, },
}
Note: read - call own tag? Or Doc method?
====
PDF forms:
	* pdftk <file.pdf> generate_fdf output test.fdf - get field names into test.fdf

====
Dependencies:
	* 