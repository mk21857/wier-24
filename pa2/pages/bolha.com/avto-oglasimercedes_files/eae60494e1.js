import{g as e}from"./a20b5a7092.js";var r,t={exports:{}};r=function(e){var r=document.getElementsByTagName("script")[0];r.parentNode.insertBefore(e,r)};const n=e(t.exports=function(e,t,n){var o;t&&"function"!=typeof t&&(n=t.context||n,o=t.setup,t=t.callback);var a,c,l=document.createElement("script"),s=!1,i=function(){s||(s=!0,c(),t&&t.call(n,a))},d=function(){a=new Error(e||"EMPTY"),i()};if(l.readyState&&!("async"in l)){var f={loaded:!0,complete:!0},u=!1;c=function(){l.onreadystatechange=l.onerror=null},l.onreadystatechange=function(){var e=l.readyState;if(!a){if(!u&&f[e]&&(u=!0,r(l)),"loaded"===e&&(l.children,"loading"===l.readyState))return d();"complete"===l.readyState&&i()}},l.onerror=d,o&&o.call(n,l),l.src=e}else c=function(){l.onload=l.onerror=null},l.onerror=d,l.onload=i,l.async=!0,l.charset="utf-8",o&&o.call(n,l),l.src=e,r(l)});export{n as l};