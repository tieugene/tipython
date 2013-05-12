var menu=function() {
	function dd(n) {
		this.n=n;
		this.c=[]
	}
	dd.prototype.init=function(n) {
		var s=document.getElementById(n).getElementsByTagName('ul'), l=s.length, i=0;
		for (i; i<l; i++) {
			var h=s[i].parentNode;
			this.c[i]=s[i];
			h.onmouseover=new Function(this.n+'.ss('+i+')');
			h.onmouseout=new Function(this.n+'.sh('+i+')');
		}
	}
	dd.prototype.ss=function(i) { this.c[i].style.display='block'; }
	dd.prototype.sh=function(i) { this.c[i].style.display='none'; }
	return{dd:dd}
}();