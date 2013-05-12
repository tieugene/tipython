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
