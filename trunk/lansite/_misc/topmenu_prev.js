function setmenu (menu_id) {
	/* open submenu and set colors;
	menu_id - li's id
	- replace a w/ text in 1st anchor below
	while not top:
		- expand 1st ul below (if exists)
		- set active class of self
		- switch to parent.parent (prev level's li)
	*/
	
	var l = document.getElementById(menu_id);
	// l.getElementByTagName('ul')[0].style.display = "block";	// replace anchor w/ text
	do {
		uls = l.getElementsByTagName('ul');
		if (uls.length > 0) {
			uls[0].style.display = "block";		// expand ul below FIXME: if exists
		}
		l.className = "active";					// highlight current li
		if (l.parentNode.className != "topmenu") {
			l = l.parentNode.parentNode
		} else {
			l = 0;
		}
	} while(l != 0);
}
