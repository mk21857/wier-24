var t=function(t){return t.replace(/^[\s\uFEFF\u00A0]+/,"")},e=function(t){for(var e=t.length;/[\s\uFEFF\u00A0]/.test(t[e-1]);)e--;return t.slice(0,e)},r=function(t){return t.replace(/^[\r\n]+/,"")},n=function(t){return t.replace(/[\r\n]+$/,"")},o=/<([a-z][^\/\0>\x20\t\r\n\f]*)/i,a=/<\s*\w.*?>/g;function l(o){for(var a=arguments.length,l=new Array(a>1?a-1:0),u=1;u<a;u++)l[u-1]=arguments[u];var c=[].concat(o.raw),d=c.length;return c[0]=t(r(c[0])),c[d-1]=e(n(c[d-1])),c.reduce((function(t,e,r){var n=l[r-1];return Array.isArray(n)&&(n=n.join("")),t+n+e}))}function u(t){var e={option:[1,'<select multiple="multiple">',"</select>"],legend:[1,"<fieldset>","</fieldset>"],area:[1,"<map>","</map>"],param:[1,"<object>","</object>"],thead:[1,"<table>","</table>"],tr:[2,"<table><tbody>","</tbody></table>"],col:[2,"<table><tbody></tbody><colgroup>","</colgroup></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],_default:[0,"",""]};e.optgroup=e.option,e.tbody=e.tfoot=e.colgroup=e.caption=e.thead,e.th=e.td;var r=document.createElement("div"),n=a.exec(t);if(a.lastIndex=0,null!==n){var l=e[(o.exec(n[0])||[e._default[1],e._default[2]])[1].toLowerCase()]||e._default;r.innerHTML=l[1]+t+l[2];for(var u=l[0]+1;u--;)if(r=r.lastChild,0===u&&r.parentNode&&r.parentNode.childNodes.length>1)throw new Error("Only one root element is allowed.")}else r.innerHTML=t,r=r.lastChild;return r}function c(){return u(l.apply(void 0,arguments))}const d=function(t){return u(n(r(t)).trim())};export{d,c as t};
