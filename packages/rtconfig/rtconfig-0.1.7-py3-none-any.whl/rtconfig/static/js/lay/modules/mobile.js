/** layui-v2.4.3 MIT License By https://www.layui.com */
 ;layui.define(function(i){i("layui.mobile",layui.v)});layui.define(function(e){"use strict";var r={open:"{{",close:"}}"},c={exp:function(e){return new RegExp(e,"g")},query:function(e,c,t){var o=["#([\\s\\S])+?","([^{#}])*?"][e||0];return n((c||"")+r.open+o+r.close+(t||""))},escape:function(e){return String(e||"").replace(/&(?!#?[a-zA-Z0-9]+;)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/'/g,"&#39;").replace(/"/g,"&quot;")},error:function(e,r){var c="Laytpl Error：";return"object"==typeof console&&console.error(c+e+"\n"+(r||"")),c+e}},n=c.exp,t=function(e){this.tpl=e};t.pt=t.prototype,window.errors=0,t.pt.parse=function(e,t){var o=this,p=e,a=n("^"+r.open+"#",""),l=n(r.close+"$","");e=e.replace(/\s+|\r|\t|\n/g," ").replace(n(r.open+"#"),r.open+"# ").replace(n(r.close+"}"),"} "+r.close).replace(/\\/g,"\\\\").replace(n(r.open+"!(.+?)!"+r.close),function(e){return e=e.replace(n("^"+r.open+"!"),"").replace(n("!"+r.close),"").replace(n(r.open+"|"+r.close),function(e){return e.replace(/(.)/g,"\\$1")})}).replace(/(?="|')/g,"\\").replace(c.query(),function(e){return e=e.replace(a,"").replace(l,""),'";'+e.replace(/\\/g,"")+';view+="'}).replace(c.query(1),function(e){var c='"+(';return e.replace(/\s/g,"")===r.open+r.close?"":(e=e.replace(n(r.open+"|"+r.close),""),/^=/.test(e)&&(e=e.replace(/^=/,""),c='"+_escape_('),c+e.replace(/\\/g,"")+')+"')}),e='"use strict";var view = "'+e+'";return view;';try{return o.cache=e=new Function("d, _escape_",e),e(t,c.escape)}catch(u){return delete o.cache,c.error(u,p)}},t.pt.render=function(e,r){var n,t=this;return e?(n=t.cache?t.cache(e,c.escape):t.parse(t.tpl,e),r?void r(n):n):c.error("no data")};var o=function(e){return"string"!=typeof e?c.error("Template not found"):new t(e)};o.config=function(e){e=e||{};for(var c in e)r[c]=e[c]},o.v="1.2.0",e("laytpl",o)});layui.define(function(e){"use strict";var t=(window,document),i="querySelectorAll",n="getElementsByClassName",a=function(e){return t[i](e)},s={type:0,shade:!0,shadeClose:!0,fixed:!0,anim:"scale"},l={extend:function(e){var t=JSON.parse(JSON.stringify(s));for(var i in e)t[i]=e[i];return t},timer:{},end:{}};l.touch=function(e,t){e.addEventListener("click",function(e){t.call(this,e)},!1)};var o=0,r=["layui-m-layer"],d=function(e){var t=this;t.config=l.extend(e),t.view()};d.prototype.view=function(){var e=this,i=e.config,s=t.createElement("div");e.id=s.id=r[0]+o,s.setAttribute("class",r[0]+" "+r[0]+(i.type||0)),s.setAttribute("index",o);var l=function(){var e="object"==typeof i.title;return i.title?'<h3 style="'+(e?i.title[1]:"")+'">'+(e?i.title[0]:i.title)+"</h3>":""}(),d=function(){"string"==typeof i.btn&&(i.btn=[i.btn]);var e,t=(i.btn||[]).length;return 0!==t&&i.btn?(e='<span yes type="1">'+i.btn[0]+"</span>",2===t&&(e='<span no type="0">'+i.btn[1]+"</span>"+e),'<div class="layui-m-layerbtn">'+e+"</div>"):""}();if(i.fixed||(i.top=i.hasOwnProperty("top")?i.top:100,i.style=i.style||"",i.style+=" top:"+(t.body.scrollTop+i.top)+"px"),2===i.type&&(i.content='<i></i><i class="layui-m-layerload"></i><i></i><p>'+(i.content||"")+"</p>"),i.skin&&(i.anim="up"),"msg"===i.skin&&(i.shade=!1),s.innerHTML=(i.shade?"<div "+("string"==typeof i.shade?'style="'+i.shade+'"':"")+' class="layui-m-layershade"></div>':"")+'<div class="layui-m-layermain" '+(i.fixed?"":'style="position:static;"')+'><div class="layui-m-layersection"><div class="layui-m-layerchild '+(i.skin?"layui-m-layer-"+i.skin+" ":"")+(i.className?i.className:"")+" "+(i.anim?"layui-m-anim-"+i.anim:"")+'" '+(i.style?'style="'+i.style+'"':"")+">"+l+'<div class="layui-m-layercont">'+i.content+"</div>"+d+"</div></div></div>",!i.type||2===i.type){var y=t[n](r[0]+i.type),u=y.length;u>=1&&c.close(y[0].getAttribute("index"))}document.body.appendChild(s);var m=e.elem=a("#"+e.id)[0];i.success&&i.success(m),e.index=o++,e.action(i,m)},d.prototype.action=function(e,t){var i=this;e.time&&(l.timer[i.index]=setTimeout(function(){c.close(i.index)},1e3*e.time));var a=function(){var t=this.getAttribute("type");0==t?(e.no&&e.no(),c.close(i.index)):e.yes?e.yes(i.index):c.close(i.index)};if(e.btn)for(var s=t[n]("layui-m-layerbtn")[0].children,o=s.length,r=0;r<o;r++)l.touch(s[r],a);if(e.shade&&e.shadeClose){var d=t[n]("layui-m-layershade")[0];l.touch(d,function(){c.close(i.index,e.end)})}e.end&&(l.end[i.index]=e.end)};var c={v:"2.0 m",index:o,open:function(e){var t=new d(e||{});return t.index},close:function(e){var i=a("#"+r[0]+e)[0];i&&(i.innerHTML="",t.body.removeChild(i),clearTimeout(l.timer[e]),delete l.timer[e],"function"==typeof l.end[e]&&l.end[e](),delete l.end[e])},closeAll:function(){for(var e=t[n](r[0]),i=0,a=e.length;i<a;i++)c.close(0|e[0].getAttribute("index"))}};e("layer-mobile",c)});layui.define(function(t){var e=function(){function t(t){return null==t?String(t):J[W.call(t)]||"object"}function e(e){return"function"==t(e)}function n(t){return null!=t&&t==t.window}function r(t){return null!=t&&t.nodeType==t.DOCUMENT_NODE}function i(e){return"object"==t(e)}function o(t){return i(t)&&!n(t)&&Object.getPrototypeOf(t)==Object.prototype}function a(t){var e=!!t&&"length"in t&&t.length,r=T.type(t);return"function"!=r&&!n(t)&&("array"==r||0===e||"number"==typeof e&&e>0&&e-1 in t)}function s(t){return A.call(t,function(t){return null!=t})}function u(t){return t.length>0?T.fn.concat.apply([],t):t}function c(t){return t.replace(/::/g,"/").replace(/([A-Z]+)([A-Z][a-z])/g,"$1_$2").replace(/([a-z\d])([A-Z])/g,"$1_$2").replace(/_/g,"-").toLowerCase()}function l(t){return t in F?F[t]:F[t]=new RegExp("(^|\\s)"+t+"(\\s|$)")}function f(t,e){return"number"!=typeof e||k[c(t)]?e:e+"px"}function h(t){var e,n;return $[t]||(e=L.createElement(t),L.body.appendChild(e),n=getComputedStyle(e,"").getPropertyValue("display"),e.parentNode.removeChild(e),"none"==n&&(n="block"),$[t]=n),$[t]}function p(t){return"children"in t?D.call(t.children):T.map(t.childNodes,function(t){if(1==t.nodeType)return t})}function d(t,e){var n,r=t?t.length:0;for(n=0;n<r;n++)this[n]=t[n];this.length=r,this.selector=e||""}function m(t,e,n){for(j in e)n&&(o(e[j])||Q(e[j]))?(o(e[j])&&!o(t[j])&&(t[j]={}),Q(e[j])&&!Q(t[j])&&(t[j]=[]),m(t[j],e[j],n)):e[j]!==E&&(t[j]=e[j])}function v(t,e){return null==e?T(t):T(t).filter(e)}function g(t,n,r,i){return e(n)?n.call(t,r,i):n}function y(t,e,n){null==n?t.removeAttribute(e):t.setAttribute(e,n)}function x(t,e){var n=t.className||"",r=n&&n.baseVal!==E;return e===E?r?n.baseVal:n:void(r?n.baseVal=e:t.className=e)}function b(t){try{return t?"true"==t||"false"!=t&&("null"==t?null:+t+""==t?+t:/^[\[\{]/.test(t)?T.parseJSON(t):t):t}catch(e){return t}}function w(t,e){e(t);for(var n=0,r=t.childNodes.length;n<r;n++)w(t.childNodes[n],e)}var E,j,T,S,C,N,O=[],P=O.concat,A=O.filter,D=O.slice,L=window.document,$={},F={},k={"column-count":1,columns:1,"font-weight":1,"line-height":1,opacity:1,"z-index":1,zoom:1},M=/^\s*<(\w+|!)[^>]*>/,R=/^<(\w+)\s*\/?>(?:<\/\1>|)$/,z=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi,Z=/^(?:body|html)$/i,q=/([A-Z])/g,H=["val","css","html","text","data","width","height","offset"],I=["after","prepend","before","append"],V=L.createElement("table"),_=L.createElement("tr"),B={tr:L.createElement("tbody"),tbody:V,thead:V,tfoot:V,td:_,th:_,"*":L.createElement("div")},U=/complete|loaded|interactive/,X=/^[\w-]*$/,J={},W=J.toString,Y={},G=L.createElement("div"),K={tabindex:"tabIndex",readonly:"readOnly","for":"htmlFor","class":"className",maxlength:"maxLength",cellspacing:"cellSpacing",cellpadding:"cellPadding",rowspan:"rowSpan",colspan:"colSpan",usemap:"useMap",frameborder:"frameBorder",contenteditable:"contentEditable"},Q=Array.isArray||function(t){return t instanceof Array};return Y.matches=function(t,e){if(!e||!t||1!==t.nodeType)return!1;var n=t.matches||t.webkitMatchesSelector||t.mozMatchesSelector||t.oMatchesSelector||t.matchesSelector;if(n)return n.call(t,e);var r,i=t.parentNode,o=!i;return o&&(i=G).appendChild(t),r=~Y.qsa(i,e).indexOf(t),o&&G.removeChild(t),r},C=function(t){return t.replace(/-+(.)?/g,function(t,e){return e?e.toUpperCase():""})},N=function(t){return A.call(t,function(e,n){return t.indexOf(e)==n})},Y.fragment=function(t,e,n){var r,i,a;return R.test(t)&&(r=T(L.createElement(RegExp.$1))),r||(t.replace&&(t=t.replace(z,"<$1></$2>")),e===E&&(e=M.test(t)&&RegExp.$1),e in B||(e="*"),a=B[e],a.innerHTML=""+t,r=T.each(D.call(a.childNodes),function(){a.removeChild(this)})),o(n)&&(i=T(r),T.each(n,function(t,e){H.indexOf(t)>-1?i[t](e):i.attr(t,e)})),r},Y.Z=function(t,e){return new d(t,e)},Y.isZ=function(t){return t instanceof Y.Z},Y.init=function(t,n){var r;if(!t)return Y.Z();if("string"==typeof t)if(t=t.trim(),"<"==t[0]&&M.test(t))r=Y.fragment(t,RegExp.$1,n),t=null;else{if(n!==E)return T(n).find(t);r=Y.qsa(L,t)}else{if(e(t))return T(L).ready(t);if(Y.isZ(t))return t;if(Q(t))r=s(t);else if(i(t))r=[t],t=null;else if(M.test(t))r=Y.fragment(t.trim(),RegExp.$1,n),t=null;else{if(n!==E)return T(n).find(t);r=Y.qsa(L,t)}}return Y.Z(r,t)},T=function(t,e){return Y.init(t,e)},T.extend=function(t){var e,n=D.call(arguments,1);return"boolean"==typeof t&&(e=t,t=n.shift()),n.forEach(function(n){m(t,n,e)}),t},Y.qsa=function(t,e){var n,r="#"==e[0],i=!r&&"."==e[0],o=r||i?e.slice(1):e,a=X.test(o);return t.getElementById&&a&&r?(n=t.getElementById(o))?[n]:[]:1!==t.nodeType&&9!==t.nodeType&&11!==t.nodeType?[]:D.call(a&&!r&&t.getElementsByClassName?i?t.getElementsByClassName(o):t.getElementsByTagName(e):t.querySelectorAll(e))},T.contains=L.documentElement.contains?function(t,e){return t!==e&&t.contains(e)}:function(t,e){for(;e&&(e=e.parentNode);)if(e===t)return!0;return!1},T.type=t,T.isFunction=e,T.isWindow=n,T.isArray=Q,T.isPlainObject=o,T.isEmptyObject=function(t){var e;for(e in t)return!1;return!0},T.isNumeric=function(t){var e=Number(t),n=typeof t;return null!=t&&"boolean"!=n&&("string"!=n||t.length)&&!isNaN(e)&&isFinite(e)||!1},T.inArray=function(t,e,n){return O.indexOf.call(e,t,n)},T.camelCase=C,T.trim=function(t){return null==t?"":String.prototype.trim.call(t)},T.uuid=0,T.support={},T.expr={},T.noop=function(){},T.map=function(t,e){var n,r,i,o=[];if(a(t))for(r=0;r<t.length;r++)n=e(t[r],r),null!=n&&o.push(n);else for(i in t)n=e(t[i],i),null!=n&&o.push(n);return u(o)},T.each=function(t,e){var n,r;if(a(t)){for(n=0;n<t.length;n++)if(e.call(t[n],n,t[n])===!1)return t}else for(r in t)if(e.call(t[r],r,t[r])===!1)return t;return t},T.grep=function(t,e){return A.call(t,e)},window.JSON&&(T.parseJSON=JSON.parse),T.each("Boolean Number String Function Array Date RegExp Object Error".split(" "),function(t,e){J["[object "+e+"]"]=e.toLowerCase()}),T.fn={constructor:Y.Z,length:0,forEach:O.forEach,reduce:O.reduce,push:O.push,sort:O.sort,splice:O.splice,indexOf:O.indexOf,concat:function(){var t,e,n=[];for(t=0;t<arguments.length;t++)e=arguments[t],n[t]=Y.isZ(e)?e.toArray():e;return P.apply(Y.isZ(this)?this.toArray():this,n)},map:function(t){return T(T.map(this,function(e,n){return t.call(e,n,e)}))},slice:function(){return T(D.apply(this,arguments))},ready:function(t){return U.test(L.readyState)&&L.body?t(T):L.addEventListener("DOMContentLoaded",function(){t(T)},!1),this},get:function(t){return t===E?D.call(this):this[t>=0?t:t+this.length]},toArray:function(){return this.get()},size:function(){return this.length},remove:function(){return this.each(function(){null!=this.parentNode&&this.parentNode.removeChild(this)})},each:function(t){return O.every.call(this,function(e,n){return t.call(e,n,e)!==!1}),this},filter:function(t){return e(t)?this.not(this.not(t)):T(A.call(this,function(e){return Y.matches(e,t)}))},add:function(t,e){return T(N(this.concat(T(t,e))))},is:function(t){return this.length>0&&Y.matches(this[0],t)},not:function(t){var n=[];if(e(t)&&t.call!==E)this.each(function(e){t.call(this,e)||n.push(this)});else{var r="string"==typeof t?this.filter(t):a(t)&&e(t.item)?D.call(t):T(t);this.forEach(function(t){r.indexOf(t)<0&&n.push(t)})}return T(n)},has:function(t){return this.filter(function(){return i(t)?T.contains(this,t):T(this).find(t).size()})},eq:function(t){return t===-1?this.slice(t):this.slice(t,+t+1)},first:function(){var t=this[0];return t&&!i(t)?t:T(t)},last:function(){var t=this[this.length-1];return t&&!i(t)?t:T(t)},find:function(t){var e,n=this;return e=t?"object"==typeof t?T(t).filter(function(){var t=this;return O.some.call(n,function(e){return T.contains(e,t)})}):1==this.length?T(Y.qsa(this[0],t)):this.map(function(){return Y.qsa(this,t)}):T()},closest:function(t,e){var n=[],i="object"==typeof t&&T(t);return this.each(function(o,a){for(;a&&!(i?i.indexOf(a)>=0:Y.matches(a,t));)a=a!==e&&!r(a)&&a.parentNode;a&&n.indexOf(a)<0&&n.push(a)}),T(n)},parents:function(t){for(var e=[],n=this;n.length>0;)n=T.map(n,function(t){if((t=t.parentNode)&&!r(t)&&e.indexOf(t)<0)return e.push(t),t});return v(e,t)},parent:function(t){return v(N(this.pluck("parentNode")),t)},children:function(t){return v(this.map(function(){return p(this)}),t)},contents:function(){return this.map(function(){return this.contentDocument||D.call(this.childNodes)})},siblings:function(t){return v(this.map(function(t,e){return A.call(p(e.parentNode),function(t){return t!==e})}),t)},empty:function(){return this.each(function(){this.innerHTML=""})},pluck:function(t){return T.map(this,function(e){return e[t]})},show:function(){return this.each(function(){"none"==this.style.display&&(this.style.display=""),"none"==getComputedStyle(this,"").getPropertyValue("display")&&(this.style.display=h(this.nodeName))})},replaceWith:function(t){return this.before(t).remove()},wrap:function(t){var n=e(t);if(this[0]&&!n)var r=T(t).get(0),i=r.parentNode||this.length>1;return this.each(function(e){T(this).wrapAll(n?t.call(this,e):i?r.cloneNode(!0):r)})},wrapAll:function(t){if(this[0]){T(this[0]).before(t=T(t));for(var e;(e=t.children()).length;)t=e.first();T(t).append(this)}return this},wrapInner:function(t){var n=e(t);return this.each(function(e){var r=T(this),i=r.contents(),o=n?t.call(this,e):t;i.length?i.wrapAll(o):r.append(o)})},unwrap:function(){return this.parent().each(function(){T(this).replaceWith(T(this).children())}),this},clone:function(){return this.map(function(){return this.cloneNode(!0)})},hide:function(){return this.css("display","none")},toggle:function(t){return this.each(function(){var e=T(this);(t===E?"none"==e.css("display"):t)?e.show():e.hide()})},prev:function(t){return T(this.pluck("previousElementSibling")).filter(t||"*")},next:function(t){return T(this.pluck("nextElementSibling")).filter(t||"*")},html:function(t){return 0 in arguments?this.each(function(e){var n=this.innerHTML;T(this).empty().append(g(this,t,e,n))}):0 in this?this[0].innerHTML:null},text:function(t){return 0 in arguments?this.each(function(e){var n=g(this,t,e,this.textContent);this.textContent=null==n?"":""+n}):0 in this?this.pluck("textContent").join(""):null},attr:function(t,e){var n;return"string"!=typeof t||1 in arguments?this.each(function(n){if(1===this.nodeType)if(i(t))for(j in t)y(this,j,t[j]);else y(this,t,g(this,e,n,this.getAttribute(t)))}):0 in this&&1==this[0].nodeType&&null!=(n=this[0].getAttribute(t))?n:E},removeAttr:function(t){return this.each(function(){1===this.nodeType&&t.split(" ").forEach(function(t){y(this,t)},this)})},prop:function(t,e){return t=K[t]||t,1 in arguments?this.each(function(n){this[t]=g(this,e,n,this[t])}):this[0]&&this[0][t]},removeProp:function(t){return t=K[t]||t,this.each(function(){delete this[t]})},data:function(t,e){var n="data-"+t.replace(q,"-$1").toLowerCase(),r=1 in arguments?this.attr(n,e):this.attr(n);return null!==r?b(r):E},val:function(t){return 0 in arguments?(null==t&&(t=""),this.each(function(e){this.value=g(this,t,e,this.value)})):this[0]&&(this[0].multiple?T(this[0]).find("option").filter(function(){return this.selected}).pluck("value"):this[0].value)},offset:function(t){if(t)return this.each(function(e){var n=T(this),r=g(this,t,e,n.offset()),i=n.offsetParent().offset(),o={top:r.top-i.top,left:r.left-i.left};"static"==n.css("position")&&(o.position="relative"),n.css(o)});if(!this.length)return null;if(L.documentElement!==this[0]&&!T.contains(L.documentElement,this[0]))return{top:0,left:0};var e=this[0].getBoundingClientRect();return{left:e.left+window.pageXOffset,top:e.top+window.pageYOffset,width:Math.round(e.width),height:Math.round(e.height)}},css:function(e,n){if(arguments.length<2){var r=this[0];if("string"==typeof e){if(!r)return;return r.style[C(e)]||getComputedStyle(r,"").getPropertyValue(e)}if(Q(e)){if(!r)return;var i={},o=getComputedStyle(r,"");return T.each(e,function(t,e){i[e]=r.style[C(e)]||o.getPropertyValue(e)}),i}}var a="";if("string"==t(e))n||0===n?a=c(e)+":"+f(e,n):this.each(function(){this.style.removeProperty(c(e))});else for(j in e)e[j]||0===e[j]?a+=c(j)+":"+f(j,e[j])+";":this.each(function(){this.style.removeProperty(c(j))});return this.each(function(){this.style.cssText+=";"+a})},index:function(t){return t?this.indexOf(T(t)[0]):this.parent().children().indexOf(this[0])},hasClass:function(t){return!!t&&O.some.call(this,function(t){return this.test(x(t))},l(t))},addClass:function(t){return t?this.each(function(e){if("className"in this){S=[];var n=x(this),r=g(this,t,e,n);r.split(/\s+/g).forEach(function(t){T(this).hasClass(t)||S.push(t)},this),S.length&&x(this,n+(n?" ":"")+S.join(" "))}}):this},removeClass:function(t){return this.each(function(e){if("className"in this){if(t===E)return x(this,"");S=x(this),g(this,t,e,S).split(/\s+/g).forEach(function(t){S=S.replace(l(t)," ")}),x(this,S.trim())}})},toggleClass:function(t,e){return t?this.each(function(n){var r=T(this),i=g(this,t,n,x(this));i.split(/\s+/g).forEach(function(t){(e===E?!r.hasClass(t):e)?r.addClass(t):r.removeClass(t)})}):this},scrollTop:function(t){if(this.length){var e="scrollTop"in this[0];return t===E?e?this[0].scrollTop:this[0].pageYOffset:this.each(e?function(){this.scrollTop=t}:function(){this.scrollTo(this.scrollX,t)})}},scrollLeft:function(t){if(this.length){var e="scrollLeft"in this[0];return t===E?e?this[0].scrollLeft:this[0].pageXOffset:this.each(e?function(){this.scrollLeft=t}:function(){this.scrollTo(t,this.scrollY)})}},position:function(){if(this.length){var t=this[0],e=this.offsetParent(),n=this.offset(),r=Z.test(e[0].nodeName)?{top:0,left:0}:e.offset();return n.top-=parseFloat(T(t).css("margin-top"))||0,n.left-=parseFloat(T(t).css("margin-left"))||0,r.top+=parseFloat(T(e[0]).css("border-top-width"))||0,r.left+=parseFloat(T(e[0]).css("border-left-width"))||0,{top:n.top-r.top,left:n.left-r.left}}},offsetParent:function(){return this.map(function(){for(var t=this.offsetParent||L.body;t&&!Z.test(t.nodeName)&&"static"==T(t).css("position");)t=t.offsetParent;return t})}},T.fn.detach=T.fn.remove,["width","height"].forEach(function(t){var e=t.replace(/./,function(t){return t[0].toUpperCase()});T.fn[t]=function(i){var o,a=this[0];return i===E?n(a)?a["inner"+e]:r(a)?a.documentElement["scroll"+e]:(o=this.offset())&&o[t]:this.each(function(e){a=T(this),a.css(t,g(this,i,e,a[t]()))})}}),I.forEach(function(e,n){var r=n%2;T.fn[e]=function(){var e,i,o=T.map(arguments,function(n){var r=[];return e=t(n),"array"==e?(n.forEach(function(t){return t.nodeType!==E?r.push(t):T.zepto.isZ(t)?r=r.concat(t.get()):void(r=r.concat(Y.fragment(t)))}),r):"object"==e||null==n?n:Y.fragment(n)}),a=this.length>1;return o.length<1?this:this.each(function(t,e){i=r?e:e.parentNode,e=0==n?e.nextSibling:1==n?e.firstChild:2==n?e:null;var s=T.contains(L.documentElement,i);o.forEach(function(t){if(a)t=t.cloneNode(!0);else if(!i)return T(t).remove();i.insertBefore(t,e),s&&w(t,function(t){if(!(null==t.nodeName||"SCRIPT"!==t.nodeName.toUpperCase()||t.type&&"text/javascript"!==t.type||t.src)){var e=t.ownerDocument?t.ownerDocument.defaultView:window;e.eval.call(e,t.innerHTML)}})})})},T.fn[r?e+"To":"insert"+(n?"Before":"After")]=function(t){return T(t)[e](this),this}}),Y.Z.prototype=d.prototype=T.fn,Y.uniq=N,Y.deserializeValue=b,T.zepto=Y,T}();!function(t){function e(t){return t._zid||(t._zid=h++)}function n(t,n,o,a){if(n=r(n),n.ns)var s=i(n.ns);return(v[e(t)]||[]).filter(function(t){return t&&(!n.e||t.e==n.e)&&(!n.ns||s.test(t.ns))&&(!o||e(t.fn)===e(o))&&(!a||t.sel==a)})}function r(t){var e=(""+t).split(".");return{e:e[0],ns:e.slice(1).sort().join(" ")}}function i(t){return new RegExp("(?:^| )"+t.replace(" "," .* ?")+"(?: |$)")}function o(t,e){return t.del&&!y&&t.e in x||!!e}function a(t){return b[t]||y&&x[t]||t}function s(n,i,s,u,l,h,p){var d=e(n),m=v[d]||(v[d]=[]);i.split(/\s/).forEach(function(e){if("ready"==e)return t(document).ready(s);var i=r(e);i.fn=s,i.sel=l,i.e in b&&(s=function(e){var n=e.relatedTarget;if(!n||n!==this&&!t.contains(this,n))return i.fn.apply(this,arguments)}),i.del=h;var d=h||s;i.proxy=function(t){if(t=c(t),!t.isImmediatePropagationStopped()){t.data=u;var e=d.apply(n,t._args==f?[t]:[t].concat(t._args));return e===!1&&(t.preventDefault(),t.stopPropagation()),e}},i.i=m.length,m.push(i),"addEventListener"in n&&n.addEventListener(a(i.e),i.proxy,o(i,p))})}function u(t,r,i,s,u){var c=e(t);(r||"").split(/\s/).forEach(function(e){n(t,e,i,s).forEach(function(e){delete v[c][e.i],"removeEventListener"in t&&t.removeEventListener(a(e.e),e.proxy,o(e,u))})})}function c(e,n){return!n&&e.isDefaultPrevented||(n||(n=e),t.each(T,function(t,r){var i=n[t];e[t]=function(){return this[r]=w,i&&i.apply(n,arguments)},e[r]=E}),e.timeStamp||(e.timeStamp=Date.now()),(n.defaultPrevented!==f?n.defaultPrevented:"returnValue"in n?n.returnValue===!1:n.getPreventDefault&&n.getPreventDefault())&&(e.isDefaultPrevented=w)),e}function l(t){var e,n={originalEvent:t};for(e in t)j.test(e)||t[e]===f||(n[e]=t[e]);return c(n,t)}var f,h=1,p=Array.prototype.slice,d=t.isFunction,m=function(t){return"string"==typeof t},v={},g={},y="onfocusin"in window,x={focus:"focusin",blur:"focusout"},b={mouseenter:"mouseover",mouseleave:"mouseout"};g.click=g.mousedown=g.mouseup=g.mousemove="MouseEvents",t.event={add:s,remove:u},t.proxy=function(n,r){var i=2 in arguments&&p.call(arguments,2);if(d(n)){var o=function(){return n.apply(r,i?i.concat(p.call(arguments)):arguments)};return o._zid=e(n),o}if(m(r))return i?(i.unshift(n[r],n),t.proxy.apply(null,i)):t.proxy(n[r],n);throw new TypeError("expected function")},t.fn.bind=function(t,e,n){return this.on(t,e,n)},t.fn.unbind=function(t,e){return this.off(t,e)},t.fn.one=function(t,e,n,r){return this.on(t,e,n,r,1)};var w=function(){return!0},E=function(){return!1},j=/^([A-Z]|returnValue$|layer[XY]$|webkitMovement[XY]$)/,T={preventDefault:"isDefaultPrevented",stopImmediatePropagation:"isImmediatePropagationStopped",stopPropagation:"isPropagationStopped"};t.fn.delegate=function(t,e,n){return this.on(e,t,n)},t.fn.undelegate=function(t,e,n){return this.off(e,t,n)},t.fn.live=function(e,n){return t(document.body).delegate(this.selector,e,n),this},t.fn.die=function(e,n){return t(document.body).undelegate(this.selector,e,n),this},t.fn.on=function(e,n,r,i,o){var a,c,h=this;return e&&!m(e)?(t.each(e,function(t,e){h.on(t,n,r,e,o)}),h):(m(n)||d(i)||i===!1||(i=r,r=n,n=f),i!==f&&r!==!1||(i=r,r=f),i===!1&&(i=E),h.each(function(f,h){o&&(a=function(t){return u(h,t.type,i),i.apply(this,arguments)}),n&&(c=function(e){var r,o=t(e.target).closest(n,h).get(0);if(o&&o!==h)return r=t.extend(l(e),{currentTarget:o,liveFired:h}),(a||i).apply(o,[r].concat(p.call(arguments,1)))}),s(h,e,i,r,n,c||a)}))},t.fn.off=function(e,n,r){var i=this;return e&&!m(e)?(t.each(e,function(t,e){i.off(t,n,e)}),i):(m(n)||d(r)||r===!1||(r=n,n=f),r===!1&&(r=E),i.each(function(){u(this,e,r,n)}))},t.fn.trigger=function(e,n){return e=m(e)||t.isPlainObject(e)?t.Event(e):c(e),e._args=n,this.each(function(){e.type in x&&"function"==typeof this[e.type]?this[e.type]():"dispatchEvent"in this?this.dispatchEvent(e):t(this).triggerHandler(e,n)})},t.fn.triggerHandler=function(e,r){var i,o;return this.each(function(a,s){i=l(m(e)?t.Event(e):e),i._args=r,i.target=s,t.each(n(s,e.type||e),function(t,e){if(o=e.proxy(i),i.isImmediatePropagationStopped())return!1})}),o},"focusin focusout focus blur load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select keydown keypress keyup error".split(" ").forEach(function(e){t.fn[e]=function(t){return 0 in arguments?this.bind(e,t):this.trigger(e)}}),t.Event=function(t,e){m(t)||(e=t,t=e.type);var n=document.createEvent(g[t]||"Events"),r=!0;if(e)for(var i in e)"bubbles"==i?r=!!e[i]:n[i]=e[i];return n.initEvent(t,r,!0),c(n)}}(e),function(t){function e(e,n,r){var i=t.Event(n);return t(e).trigger(i,r),!i.isDefaultPrevented()}function n(t,n,r,i){if(t.global)return e(n||x,r,i)}function r(e){e.global&&0===t.active++&&n(e,null,"ajaxStart")}function i(e){e.global&&!--t.active&&n(e,null,"ajaxStop")}function o(t,e){var r=e.context;return e.beforeSend.call(r,t,e)!==!1&&n(e,r,"ajaxBeforeSend",[t,e])!==!1&&void n(e,r,"ajaxSend",[t,e])}function a(t,e,r,i){var o=r.context,a="success";r.success.call(o,t,a,e),i&&i.resolveWith(o,[t,a,e]),n(r,o,"ajaxSuccess",[e,r,t]),u(a,e,r)}function s(t,e,r,i,o){var a=i.context;i.error.call(a,r,e,t),o&&o.rejectWith(a,[r,e,t]),n(i,a,"ajaxError",[r,i,t||e]),u(e,r,i)}function u(t,e,r){var o=r.context;r.complete.call(o,e,t),n(r,o,"ajaxComplete",[e,r]),i(r)}function c(t,e,n){if(n.dataFilter==l)return t;var r=n.context;return n.dataFilter.call(r,t,e)}function l(){}function f(t){return t&&(t=t.split(";",2)[0]),t&&(t==T?"html":t==j?"json":w.test(t)?"script":E.test(t)&&"xml")||"text"}function h(t,e){return""==e?t:(t+"&"+e).replace(/[&?]{1,2}/,"?")}function p(e){e.processData&&e.data&&"string"!=t.type(e.data)&&(e.data=t.param(e.data,e.traditional)),!e.data||e.type&&"GET"!=e.type.toUpperCase()&&"jsonp"!=e.dataType||(e.url=h(e.url,e.data),e.data=void 0)}function d(e,n,r,i){return t.isFunction(n)&&(i=r,r=n,n=void 0),t.isFunction(r)||(i=r,r=void 0),{url:e,data:n,success:r,dataType:i}}function m(e,n,r,i){var o,a=t.isArray(n),s=t.isPlainObject(n);t.each(n,function(n,u){o=t.type(u),i&&(n=r?i:i+"["+(s||"object"==o||"array"==o?n:"")+"]"),!i&&a?e.add(u.name,u.value):"array"==o||!r&&"object"==o?m(e,u,r,n):e.add(n,u)})}var v,g,y=+new Date,x=window.document,b=/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,w=/^(?:text|application)\/javascript/i,E=/^(?:text|application)\/xml/i,j="application/json",T="text/html",S=/^\s*$/,C=x.createElement("a");C.href=window.location.href,t.active=0,t.ajaxJSONP=function(e,n){if(!("type"in e))return t.ajax(e);var r,i,u=e.jsonpCallback,c=(t.isFunction(u)?u():u)||"Zepto"+y++,l=x.createElement("script"),f=window[c],h=function(e){t(l).triggerHandler("error",e||"abort")},p={abort:h};return n&&n.promise(p),t(l).on("load error",function(o,u){clearTimeout(i),t(l).off().remove(),"error"!=o.type&&r?a(r[0],p,e,n):s(null,u||"error",p,e,n),window[c]=f,r&&t.isFunction(f)&&f(r[0]),f=r=void 0}),o(p,e)===!1?(h("abort"),p):(window[c]=function(){r=arguments},l.src=e.url.replace(/\?(.+)=\?/,"?$1="+c),x.head.appendChild(l),e.timeout>0&&(i=setTimeout(function(){h("timeout")},e.timeout)),p)},t.ajaxSettings={type:"GET",beforeSend:l,success:l,error:l,complete:l,context:null,global:!0,xhr:function(){return new window.XMLHttpRequest},accepts:{script:"text/javascript, application/javascript, application/x-javascript",json:j,xml:"application/xml, text/xml",html:T,text:"text/plain"},crossDomain:!1,timeout:0,processData:!0,cache:!0,dataFilter:l},t.ajax=function(e){var n,i,u=t.extend({},e||{}),d=t.Deferred&&t.Deferred();for(v in t.ajaxSettings)void 0===u[v]&&(u[v]=t.ajaxSettings[v]);r(u),u.crossDomain||(n=x.createElement("a"),n.href=u.url,n.href=n.href,u.crossDomain=C.protocol+"//"+C.host!=n.protocol+"//"+n.host),u.url||(u.url=window.location.toString()),(i=u.url.indexOf("#"))>-1&&(u.url=u.url.slice(0,i)),p(u);var m=u.dataType,y=/\?.+=\?/.test(u.url);if(y&&(m="jsonp"),u.cache!==!1&&(e&&e.cache===!0||"script"!=m&&"jsonp"!=m)||(u.url=h(u.url,"_="+Date.now())),"jsonp"==m)return y||(u.url=h(u.url,u.jsonp?u.jsonp+"=?":u.jsonp===!1?"":"callback=?")),t.ajaxJSONP(u,d);var b,w=u.accepts[m],E={},j=function(t,e){E[t.toLowerCase()]=[t,e]},T=/^([\w-]+:)\/\//.test(u.url)?RegExp.$1:window.location.protocol,N=u.xhr(),O=N.setRequestHeader;if(d&&d.promise(N),u.crossDomain||j("X-Requested-With","XMLHttpRequest"),j("Accept",w||"*/*"),(w=u.mimeType||w)&&(w.indexOf(",")>-1&&(w=w.split(",",2)[0]),N.overrideMimeType&&N.overrideMimeType(w)),(u.contentType||u.contentType!==!1&&u.data&&"GET"!=u.type.toUpperCase())&&j("Content-Type",u.contentType||"application/x-www-form-urlencoded"),u.headers)for(g in u.headers)j(g,u.headers[g]);if(N.setRequestHeader=j,N.onreadystatechange=function(){if(4==N.readyState){N.onreadystatechange=l,clearTimeout(b);var e,n=!1;if(N.status>=200&&N.status<300||304==N.status||0==N.status&&"file:"==T){if(m=m||f(u.mimeType||N.getResponseHeader("content-type")),"arraybuffer"==N.responseType||"blob"==N.responseType)e=N.response;else{e=N.responseText;try{e=c(e,m,u),"script"==m?(0,eval)(e):"xml"==m?e=N.responseXML:"json"==m&&(e=S.test(e)?null:t.parseJSON(e))}catch(r){n=r}if(n)return s(n,"parsererror",N,u,d)}a(e,N,u,d)}else s(N.statusText||null,N.status?"error":"abort",N,u,d)}},o(N,u)===!1)return N.abort(),s(null,"abort",N,u,d),N;var P=!("async"in u)||u.async;if(N.open(u.type,u.url,P,u.username,u.password),u.xhrFields)for(g in u.xhrFields)N[g]=u.xhrFields[g];for(g in E)O.apply(N,E[g]);return u.timeout>0&&(b=setTimeout(function(){N.onreadystatechange=l,N.abort(),s(null,"timeout",N,u,d)},u.timeout)),N.send(u.data?u.data:null),N},t.get=function(){return t.ajax(d.apply(null,arguments))},t.post=function(){var e=d.apply(null,arguments);return e.type="POST",t.ajax(e)},t.getJSON=function(){var e=d.apply(null,arguments);return e.dataType="json",t.ajax(e)},t.fn.load=function(e,n,r){if(!this.length)return this;var i,o=this,a=e.split(/\s/),s=d(e,n,r),u=s.success;return a.length>1&&(s.url=a[0],i=a[1]),s.success=function(e){o.html(i?t("<div>").html(e.replace(b,"")).find(i):e),u&&u.apply(o,arguments)},t.ajax(s),this};var N=encodeURIComponent;t.param=function(e,n){var r=[];return r.add=function(e,n){t.isFunction(n)&&(n=n()),null==n&&(n=""),this.push(N(e)+"="+N(n))},m(r,e,n),r.join("&").replace(/%20/g,"+")}}(e),function(t){t.fn.serializeArray=function(){var e,n,r=[],i=function(t){return t.forEach?t.forEach(i):void r.push({name:e,value:t})};return this[0]&&t.each(this[0].elements,function(r,o){n=o.type,e=o.name,e&&"fieldset"!=o.nodeName.toLowerCase()&&!o.disabled&&"submit"!=n&&"reset"!=n&&"button"!=n&&"file"!=n&&("radio"!=n&&"checkbox"!=n||o.checked)&&i(t(o).val())}),r},t.fn.serialize=function(){var t=[];return this.serializeArray().forEach(function(e){t.push(encodeURIComponent(e.name)+"="+encodeURIComponent(e.value))}),t.join("&")},t.fn.submit=function(e){if(0 in arguments)this.bind("submit",e);else if(this.length){var n=t.Event("submit");this.eq(0).trigger(n),n.isDefaultPrevented()||this.get(0).submit()}return this}}(e),function(){try{getComputedStyle(void 0)}catch(t){var e=getComputedStyle;window.getComputedStyle=function(t,n){try{return e(t,n)}catch(r){return null}}}}(),t("zepto",e)});layui.define(["layer-mobile","zepto"],function(e){"use strict";var t=layui.zepto,a=layui["layer-mobile"],i=(layui.device(),"layui-upload-enter"),n="layui-upload-iframe",r={icon:2,shift:6},o={file:"文件",video:"视频",audio:"音频"};a.msg=function(e){return a.open({content:e||"",skin:"msg",time:2})};var s=function(e){this.options=e};s.prototype.init=function(){var e=this,a=e.options,r=t("body"),s=t(a.elem||".layui-upload-file"),u=t('<iframe id="'+n+'" class="'+n+'" name="'+n+'"></iframe>');return t("#"+n)[0]||r.append(u),s.each(function(r,s){s=t(s);var u='<form target="'+n+'" method="'+(a.method||"post")+'" key="set-mine" enctype="multipart/form-data" action="'+(a.url||"")+'"></form>',l=s.attr("lay-type")||a.type;a.unwrap||(u='<div class="layui-box layui-upload-button">'+u+'<span class="layui-upload-icon"><i class="layui-icon">&#xe608;</i>'+(s.attr("lay-title")||a.title||"上传"+(o[l]||"图片"))+"</span></div>"),u=t(u),a.unwrap||u.on("dragover",function(e){e.preventDefault(),t(this).addClass(i)}).on("dragleave",function(){t(this).removeClass(i)}).on("drop",function(){t(this).removeClass(i)}),s.parent("form").attr("target")===n&&(a.unwrap?s.unwrap():(s.parent().next().remove(),s.unwrap().unwrap())),s.wrap(u),s.off("change").on("change",function(){e.action(this,l)})})},s.prototype.action=function(e,i){var o=this,s=o.options,u=e.value,l=t(e),p=l.attr("lay-ext")||s.ext||"";if(u){switch(i){case"file":if(p&&!RegExp("\\w\\.("+p+")$","i").test(escape(u)))return a.msg("不支持该文件格式",r),e.value="";break;case"video":if(!RegExp("\\w\\.("+(p||"avi|mp4|wma|rmvb|rm|flash|3gp|flv")+")$","i").test(escape(u)))return a.msg("不支持该视频格式",r),e.value="";break;case"audio":if(!RegExp("\\w\\.("+(p||"mp3|wav|mid")+")$","i").test(escape(u)))return a.msg("不支持该音频格式",r),e.value="";break;default:if(!RegExp("\\w\\.("+(p||"jpg|png|gif|bmp|jpeg")+")$","i").test(escape(u)))return a.msg("不支持该图片格式",r),e.value=""}s.before&&s.before(e),l.parent().submit();var c=t("#"+n),f=setInterval(function(){var t;try{t=c.contents().find("body").text()}catch(i){a.msg("上传接口存在跨域",r),clearInterval(f)}if(t){clearInterval(f),c.contents().find("body").html("");try{t=JSON.parse(t)}catch(i){return t={},a.msg("请对上传接口返回JSON字符",r)}"function"==typeof s.success&&s.success(t,e)}},30);e.value=""}},e("upload-mobile",function(e){var t=new s(e=e||{});t.init()})});layui.define(function(i){i("layim-mobile",layui.v)});layui["layui.mobile"]||layui.config({base:layui.cache.dir+"lay/modules/mobile/"}).extend({"layer-mobile":"layer-mobile",zepto:"zepto","upload-mobile":"upload-mobile","layim-mobile":"layim-mobile"}),layui.define(["layer-mobile","zepto","layim-mobile"],function(l){l("mobile",{layer:layui["layer-mobile"],layim:layui["layim-mobile"]})});