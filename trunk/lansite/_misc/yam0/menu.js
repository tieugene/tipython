/**
 *  Author: Hernan Marino <admin[at]sistemasdinamicos[dot]com[dot]ar>
 *  Date: Jul-2009
 *
 *  If you use this script, pls keep a copy of this header somewhere.
 *  You are free to use this script as you please for personal or commercial use
 **/

var the_config = {
    'node_heigth': 25, //in pixels
    'align':    'center'//centered or nothing
}

var root_x_counter = 0;
var root_y_counter = 0;
var align = 'horizontal';
var childs = {};
var roots = {'offsetL' : 0, 'offsetW' : 0};
var init_x = 0;
var init_y = 0;
var main_div = null;
var initInterval;

    var MainMenu = {
        objLevel: 0,
        objCounter: 0,
        currentParentNode: [],

        get_1 : function(el, add){
            var x = el.childNodes;
            var txt = '';
            var node;

            !add ? this.objLevel++ : '';

            for (var i=0, len=x.length; i<len; ++i){
                node = x[i];

                if (node.nodeType == 3 && node.data.replace(/\s+/g,'') != '') {//text
                    MainChilds(++this.objCounter, node, this.currentParentNode[this.objLevel - 2]);
                    MainChilds[this.objCounter].init();

                } else if (node.nodeType == 1){//element
                    var nodeTag = (node.tagName ? node.tagName.toLowerCase() : null);

                    if (nodeTag == 'a') {
                        MainChilds(++this.objCounter, node, this.currentParentNode[this.objLevel - 2]);
                        MainChilds[this.objCounter].init();

                    }else if(nodeTag == 'ul'){
                        this.currentParentNode[this.objLevel] = this.objCounter;
                        this.get_1(node);

                    }else if(nodeTag == 'li'){
                        this.get_1(node);

                    }else {
                        this.get_1(node, true);
                    }
                }
             }

             !add ? this.objLevel-- : '';
             return txt.replace(/\s+/g,' '); // Maybe trim leading
        },

        arrange: function() {
           widths = {};
           for(id in childs){
                var max_width = 0;
                for(id2 in childs[id]){
                    var o = childs[id][id2];
                    o.dive.offsetWidth > max_width ? max_width = o.dive.offsetWidth : '';
                }
                widths[id] = max_width + 45;
           }
           //window_r(widths, 3);
           for(id in childs){
               for(id2 in childs[id]){
                   var o = childs[id][id2];
                   o.dive.style.width = widths[id] + "px";
                   //to refix the witdhs of the childs of this newly fixed nodes
                   if(typeof(childs[o.id]) == 'object'){
                        //o.dive.innerHTML += '<span style="float: right;">*</span>';
                        o.dive.className = 'menu_deep';
                        for(id3 in childs[o.id]){
                            var o2 = childs[o.id][id3];
                            o2.dive.style.left = o.dive.offsetLeft + o.dive.offsetWidth + 'px';
                        }
                   }
               }
           }
        },

        arrange_main_div: function(){
            //give it the width
            //var p = main_div.parentNode;
            //alert(((roots['offsetL'] + roots['offsetW']) - init_x) + 'px');
            //p.style.width = ((roots['offsetL'] + roots['offsetW']) - init_x) + 'px';
            //p.style.height = the_config['node_heigth'];
        },

        evOnMouseOver: function(e){
            if(BrowserDetect.browser == 'Firefox'){
                var node = e.target;
            }else{
                var node = e.srcElement;
            }
            var o = MainChilds[node.id];
            o.showAllNodes();
        },

        evOnMouseOut: function(e){
            /*  1. We need to keep open only those nodes perteining to the parent of the highlighted
             *  node and all the way up until root + the childs of the current selected node
             *
           **/
            if(BrowserDetect.browser == 'Firefox'){
                var node = e.target;
            }else{
                var node = e.srcElement;
            }
            var o = MainChilds[node.id];
            o.hideAllNodes();
        },

        evOnClick: function(e){
            if(BrowserDetect.browser == 'Firefox'){
                var node = e.target;
            }else if(BrowserDetect.browser == 'Explorer'){
                var node = e.srcElement;
            }else{
                var node = e.srcElement;
            }
            var o = MainChilds[node.id];
            location.href = o.n.href;
        }

    }


    function MainChilds(the_id, node, parent){

        return MainChilds[the_id] = {
            id: the_id,
            n:  node,
            p:  parent,
            dive: null,

            myChilds : function(id, obj){
                if(typeof(childs[this.id]) == 'undefined'){
                    childs[this.id] = {};
                }
                childs[this.id][id] = obj;
            },


            showAllNodes: function(){
                //var ids = [];
                var o = this.getPar();
                while(o){
                    //ids[o.id] = true;
                    var more_ids = o.showChilds();
                    /*for (i = 0; i < more_ids.length; i++) {
                        ids[more_ids[i]] = true;
                    }*/
                    o = o.getPar();
                }
                var more_ids = MainChilds[this.id].showChilds();
                /*for (i = 0; i < more_ids.length; i++) {
                    ids[more_ids[i]] = true;
                }*/
            },

            hideAllNodes: function(){
                for (var id in MainChilds) {
                    var obj = MainChilds[id];
                    var par = MainChilds[obj.p];
                    if(typeof(par) != 'undefined'){
                        obj.dive.style.visibility = 'hidden';
                    }

                }
            },

            getX: function(){
                var p = this.getPar();
                var ret = 0;
                if(p){
                    var par_num_childs = p.numChilds();
                    if(align == 'horizontal'){
                        if(typeof(p.getPar()) == 'object'){
                            ret = (p.dive.offsetLeft + (p.dive.offsetWidth));
                        }else{
                            ret = (p.dive.offsetLeft);
                        }

                    }else{
                        //return (p.dive.offsetLeft + (70 * par_num_childs));
                    }

                }else{
                    if(align == 'horizontal'){
                        root_x_counter++;
                    }
                    //return (root_x_counter * 70);
                    ret = (roots['offsetL'] + roots['offsetW'] + 2);

                }
                return ret;
            },

            getY: function(){
                var p = this.getPar();
                var ret = 0;
                if(p){
                    var par_num_childs = p.numChilds();
                    if(align == 'horizontal'){
                        if(typeof(p.getPar()) == 'object'){
                            ret = (p.dive.offsetTop + (the_config['node_heigth'] * (par_num_childs-1)));
                        }else{
                            ret = (p.dive.offsetTop + (the_config['node_heigth'] * (par_num_childs))) + 1;
                        }
                    }

                }else{
                    if(align == 'vertical'){
                        root_y_counter++;
                    }
                    //ret = (root_y_counter * 23);
                    ret = 0
                }
                return (ret + (!p ? init_y : 0));
            },

            getPar: function(){
                return (typeof(MainChilds[this.p]) == 'object' ? MainChilds[this.p] : false);
            },

            numChilds: function(){
                var c = 0;
                for(var the_id in MainChilds){
                    var o = MainChilds[the_id];
                    if (o.id != this.id && o.p == this.id) {
                        c++;
                        this.myChilds(o.id, o);
                    }
                }
                return c;
            },

            showChilds: function(){
                var ids = [];
                for (var id in childs[this.id]) {
                    var obj = childs[this.id][id];
                    if(typeof(obj) != 'undefined'){
                        obj.dive.style.visibility = '';
                        ids[ids.length] = id;
                    }
                }
                return ids;
            },



            createDiv: function(){
                this.dive = document.createElement('div');
                this.dive.style.position = 'absolute';
                if(this.n.tagName && this.n.tagName.toLowerCase() == 'a'){
                    //window_r(this.n, 3);
                    //this.dive.style.width = this.n.innerHTML.trim().length * 7 + 'px';
                    //this.dive.innerHTML = '<a href="' + this.n.href + '" title="' + this.n.title + '" class="' + this.n.className + '">' + this.n.text + '</a>';
                    this.dive.innerHTML = this.n.innerHTML;
                    this.dive.title = this.n.title;
                    this.dive.style.cursor = 'pointer';

                    if (this.dive.addEventListener) {
                        this.dive.addEventListener('click', MainMenu.evOnClick , false);
                    }else if(this.dive.attachEvent){
                        this.dive.attachEvent('onclick', MainMenu.evOnClick);
                    }

                }else {
                    //this.dive.style.width = this.n.data.trim().length * 7 + 'px';
                    this.dive.innerHTML = this.n.data.trim();
                }

                this.dive.style.height = the_config['node_heigth'] + 'px';
                this.dive.style.border = "1px solid #ccc";
                this.dive.style.top = this.getY() + 'px';
                this.dive.style.left = this.getX() + 'px';


                this.dive.id = this.id;

                if(typeof(this.getPar()) == 'object'){
                    this.dive.style.visibility = 'hidden';
                    this.dive.className = 'menu_1';
                }else{
                    this.dive.className = 'menu_1_top';
                }

                if(typeof(this.getPar()) != 'object'){
                    this.dive.innerHTML = '&nbsp;&nbsp;&nbsp;' + this.dive.innerHTML + '&nbsp;&nbsp;&nbsp;';
                }

                document.getElementById('MenuContent').appendChild(this.dive);

                if(typeof(this.getPar()) != 'object'){
                    roots['pos'] = roots['pos'] + 1;
                    roots['offsetL'] = this.dive.offsetLeft;
                    roots['offsetW'] = this.dive.offsetWidth;
                }

                if (this.dive.addEventListener) {
                    this.dive.addEventListener('mouseover', MainMenu.evOnMouseOver, false);
                    this.dive.addEventListener('mouseout', MainMenu.evOnMouseOut, false);
                }else if(this.dive.attachEvent){
                    this.dive.attachEvent('onmouseover', MainMenu.evOnMouseOver);
                    this.dive.attachEvent('onmouseout', MainMenu.evOnMouseOut);
                }
            },

            init: function(){
                this.createDiv();
            }
        }
    }

    function Menuinit(){
        main_div = document.getElementById('MenuContent');
        //window_r(main_div, 3);
        init_x = main_div.offsetLeft;
        init_y = main_div.offsetTop;
        //alert(init_x + ' - ' + init_y);
        roots['offsetL'] = init_x;

        MainMenu.get_1(document.getElementById('Menu1'));
        MainMenu.arrange();
        MainMenu.arrange_main_div();
    }

    function addLoadEvent(func) {
        var oldonload = window.onload;
        if (typeof window.onload != 'function') {
            window.onload = func;
        } else {
            window.onload = function() {
                if (oldonload) {
                    oldonload();
                }
                func();
            }
        }
    }

    /**
     * Javascript trim functions
     */
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g,"");
    }
    String.prototype.ltrim = function() {
        return this.replace(/^\s+/,"");
    }
    String.prototype.rtrim = function() {
        return this.replace(/\s+$/,"");
    }

    function init_interval(){
        var m = document.getElementById('Menu1');
        if(m != 'null'){
            clearInterval(initInterval);
            Menuinit();
            /*clearInterval(initInterval);
            m.onreadystatechange = function(){
                if(m.readyState == 'complete'){
                    Menuinit();
                }
            }*/
        }else{
            document.write('falsooo<br />');
        }
    }

    //addLoadEvent(Menuinit);
    var b = window;
    b.onload = function(){
        initInterval = setInterval(init_interval, 200);
    };

    