// toggle.js
function Toggle(node) {
	var next = node.nextElementSibling;
	if (next.style.display == 'none') {
		next.style.display = '';
		node.innerHTML = '&#9660;'
	} else {
		next.style.display = 'none';
		node.innerHTML = '&#9654;'
	}
}

// ask2del.js
function confirmDelete(delUrl) {
	if (confirm("Are you sure you want to delete"))
		{ document.location = delUrl; }
}

// topmenu.js
function setmenu (menu_id) {
/* open submenu and set colors;
menu_id - li's id
*/
	$("#" + menu_id).addClass("active");
}

// dropdownmenu
function setdropdown (selector) {
	$(selector).find("button").click(function() {
		$(this).parent().find("div").toggle();
	});
};

function set_delete_form (url, form) {
	$("a[href=" + url + "]").click(function() {
		if (confirm('Are you sure you want to delete selected objects?'))
			document.forms[form].submit();
	});
}