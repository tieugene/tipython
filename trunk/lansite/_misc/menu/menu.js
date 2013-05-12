var timeout	= 100;
var closetimer	= 0;
var ddmenuitem	= 0;
function mopen(id)					// open hidden layer
{	
	mcancelclosetime();				// cancel close timer
	if (ddmenuitem)
		ddmenuitem.style.visibility = 'hidden';	// close old layer
	ddmenuitem = document.getElementById(id);	// get new layer and show it
	ddmenuitem.style.visibility = 'visible';
}
function mclose()					// close showed layer
	{ if (ddmenuitem) ddmenuitem.style.visibility = 'hidden'; }
function mclosetime()					// go close timer
	{ closetimer = window.setTimeout(mclose, timeout); }
function mcancelclosetime()				// cancel close timer
{
	if (closetimer)
	{
		window.clearTimeout(closetimer);
		closetimer = null;
	}
}
document.onclick = mclose;				// close layer when click-out
