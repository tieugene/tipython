/*
function select_all() {
	$("#" + $(this).attr('rel') + " INPUT[type='checkbox']").attr('checked', true);
	return false;
};

function select_none() {
	$("#" + $(this).attr('rel') + " INPUT[type='checkbox']").attr('checked', false);
	return false;
};

function invert_selection() {
	$("#" + $(this).attr('rel') + " INPUT[type='checkbox']").each( function() {
		$(this).attr('checked', !$(this).attr('checked'));
	});
	return false;
};*/

function set_selection_menu (name, menu) {
	$(menu + " a[href='#select_all']").click(function() {select_all(name, menu);});
	$(menu + " a[href='#select_none']").click(function() {select_none(name, menu);});
	$(menu + " a[href='#invert_selection']").click(function() {invert_selection(name, menu);});
	$(menu + " input:checkbox").click(function() {select_some(name, menu);});
	$("input:checkbox[name="+name+"]").click(function() {set_selector(name, menu);});
}

function set_selector (name, menu) {
	// set selector to none/some/all view
	var cb = $(menu + " input:checkbox");
	var l0 = $("input:checkbox[name="+name+"]").length;
	var l1 = $("input:checkbox[name="+name+"]:checked").length;
	cb.attr('checked', (l1 > 0));		// if select any
	if ((l1 == 0) || ( l1 == l0)) {
		cb.css({ opacity: 1 });		// if select all
		cb.attr('opacity', true);
	} else {
		cb.css({ opacity : 0.5 });	// if select not all
		cb.attr('opacity', false);
	};
}

function select_all (name, menu) {
	$("input:checkbox[name="+name+"]").attr('checked', true);
	//$(menu + " input:checkbox").attr('checked', true);
	set_selector(name, menu);
	$(menu + " div").hide();
	return false;
};

function select_none(name, menu) {
	$("input:checkbox[name="+name+"]").attr('checked', false);
	//$(menu + " input:checkbox").attr('checked', false);
	set_selector(name, menu);
	$(menu + " div").hide();
	return false;
};

function invert_selection(name, menu) {
	$("input:checkbox[name="+name+"]").each( function() {
		$(this).attr('checked', !$(this).attr('checked'));
	});
	set_selector(name, menu);
	$(menu + " div").hide();
	return false;
};

function select_some (name, menu) {
	// cb.attr('checked') already changed
	var cb = $(menu + " input:checkbox");
	if (!cb.attr('checked') && cb.attr('opacity')) {
		select_none(name, menu);
	} else {
		select_all(name, menu);
	}
	return false;
};
