var ddmenu      = 0;
function ddopen(menuid) {
	var i = document.getElementById(menuid);
	if (i.style.display == 'block') {
		i.style.display = 'none';
		ddmenu = 0;
	} else {
		if (ddmenu) {
			ddmenu.style.display = 'none';
		}
		ddmenu = i;
		ddmenu.style.display = 'block';
	}
}
function ddclose() {
	if (ddmenu)
		ddmenu.style.display = 'none';
}
// close layer when click-out
//document.onclick = ddclose;
