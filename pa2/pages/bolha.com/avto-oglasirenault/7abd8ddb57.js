import{t as a}from"./7c6ae762e4.js";import{k as l}from"./2be7671a02.js";[{locale:"hr_HR",rule:a=>1==a%10&&11!=a%100?0:a%10>=2&&a%10<=4&&(a%100<10||a%100>=20)?1:2},{locale:"sl_SI",rule:a=>1==a%100?0:2==a%100?1:3==a%100||4==a%100?2:3}].forEach((l=>{a.setPluralizationRule(l.locale,l.rule)})),a.setLocale(l).interpolateWith(/%(\w+)%/g),a.whenUndefined=(a,l)=>a,window&&window.app&&window.app.translations&&a.add(window.app.translations);const o={install(l){l.config.globalProperties.translate=a}};export{o as T};
