function setmenu (menu_id) {
	/* open submenu and set colors;
	menu_id - li's id
	- replace a w/ text in 1st anchor below
	while not top (find prev li by parent ul's idref):
		- set active class of self
		- switch to parent.parent (prev level's li)
	FIXME: search inside <div id="topmenu"> only
	*/
	// div = document.getElementById("topmenu"); */
	var l = document.getElementById(menu_id);
	//l.innerHTML = l.getElementsByTagName('a')[0].innerText;
	do {
		l.className += " active";				// highlight current li
		var p = l.parentNode.getAttribute("idref");				// upper ul->idref
		if (p !== undefined) {
			l = document.getElementById(p);
		};
	} while (p !== undefined);
}
