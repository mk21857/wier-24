import{a as e,q as t,u as r}from"./a20b5a7092.js";const s=(n="SHA-256",async(e,{outputFormat:t="hex"}={})=>{"string"==typeof e&&(e=(new globalThis.TextEncoder).encode(e));const r=await globalThis.crypto.subtle.digest(n,e);return"hex"===t?(e=>{const t=new DataView(e);let r="";for(let s=0;s<t.byteLength;s+=4)r+=t.getUint32(s).toString(16).padStart(8,"0");return r})(r):r});var n;function o(){return o=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var s in r)Object.prototype.hasOwnProperty.call(r,s)&&(e[s]=r[s])}return e},o.apply(this,arguments)}var a,i,c=(a=function(e,t){(t=e.exports=function(e){return String(e).replace(t.expr,"")}).expr=/\/+$/},a(i={exports:{}},i.exports),i.exports);function l(e){var t,r;try{return t=window[e],r="__storage_test__",t.setItem(r,r),t.removeItem(r),!0}catch(s){return s instanceof DOMException&&(22===s.code||1014===s.code||"QuotaExceededError"===s.name||"NS_ERROR_DOM_QUOTA_REACHED"===s.name&&t&&0!==t.length)}}const h="private",d="public",u="application/x-www-form-urlencoded;charset=UTF-8",p="application/vnd.api+json",y="authCredentials";class g{constructor(e){let{baseUrl:t,authType:r,userId:s,clientId:n,clientSecret:o,loggedOutUserAction:a=(()=>Promise.resolve()),apiMockServerUrl:i,apiMockServerKey:l,apiMockServerUrlsToMock:h,impersonatedUsername:d}=e;this.baseUrl=c(t),this.authType=r,this.loggedOutUserAction=a,this.clientId=n,this.clientSecret=o,this.userId=s,this.pendingAccessTokenRequest=null,this.storedCredentials=null,this.apiMockServerUrl=c(i),this.apiMockServerKey=l,this.apiMockServerUrlsToMock=h,this.impersonatedUsername=d}getStoredCredentials(){if(!l("localStorage"))return this.storedCredentials;try{const e=localStorage.getItem(y),t=JSON.parse(e),r=t.authType!==this.authType,s=this.authType===h&&t.userId!==this.userId;return r||s?(localStorage.removeItem(y),null):t}catch(e){return localStorage.removeItem(y),null}}setStoredCredentials(e){l("localStorage")&&localStorage.setItem(y,JSON.stringify(e)),this.storedCredentials=e}clearStoredCredentials(){l("localStorage")&&localStorage.removeItem(y),this.storedCredentials=null}isCcapiErrorResponse(e){return"object"==typeof e&&void 0!==e.errors&&Array.isArray(e.errors)}validateInstanceConfiguration(){function e(e,t){if(null==e)throw new TypeError(t)}e(this.authType,"Expected CCAPI authorization type."),e(this.clientId,"Expected CCAPI client id."),e(this.baseUrl,"Expected CCAPI base url."),e(this.clientSecret,"Expected an CCAPI client secret."),this.authType===h&&e(this.userId,"Expected an CCAPI user id.")}async ajax(t){let{url:r,method:s,type:n,data:a,dataType:i="json",contentType:c=p,headers:l={},rawResponse:h=!1}=t;const d=await e(r,o({method:(s||n||"GET").toUpperCase(),headers:o({},null!==c&&{"Content-Type":c},this.shouldImpersonateUser()&&{"X-Switch-User":this.impersonatedUsername},l)},a&&{body:this.prepareBody(a,c)})),u=async()=>{let e,t;try{t=i,e="json"===i?await d.json():await d.text()}catch(s){t="text",e=await d.text()}const r=new Error(d.statusText);throw r.response=d,r.status=d.status,"json"===t?r.responseJSON=e:r.responseText=e,r};if(d.ok){if(h)return d;try{return"json"===i?d.json():d.text()}catch(y){await u()}}else{if(h)throw d;await u()}}async getNewAccessToken(){return this.pendingAccessTokenRequest||(this.pendingAccessTokenRequest=this.authType===d?this.getNewAppAccessToken():this.getNewUserAccessToken(),this.clearStoredCredentials(),this.pendingAccessTokenRequest=(async()=>{try{return await this.pendingAccessTokenRequest}catch(e){throw this.authType===h&&this.isUserLoggedOut(e.status)&&await this.loggedOutUserAction(),e}finally{this.pendingAccessTokenRequest=null}})()),this.pendingAccessTokenRequest}async getNewAppAccessToken(){const e=await this.ajax({url:this.baseUrl+"/oauth2/token",method:"post",dataType:"json",contentType:u,data:{grant_type:"client_credentials",client_id:this.clientId,client_secret:this.clientSecret}}),{access_token:t}=e;return this.setStoredCredentials({authType:d,accessToken:t}),t}async getNewUserAccessToken(){const e=this.getStoredCredentials();return e&&e.refreshToken?this.getNewUserAccessTokenUsingRefreshToken():this.getNewUserAccessTokenUsingPKCE()}async getNewUserAccessTokenUsingRefreshToken(){const{refreshToken:e}=this.getStoredCredentials();try{const t=await this.ajax({url:this.baseUrl+"/oauth2/token",method:"post",dataType:"json",contentType:u,data:{client_id:this.clientId,client_secret:this.clientSecret,grant_type:"refresh_token",refresh_token:e}}),{access_token:r,refresh_token:s}=t;return this.setStoredCredentials({authType:h,userId:this.userId,accessToken:r,refreshToken:s}),r}catch(t){if(this.isNewAccessTokenNeeded(t.status))return this.getNewUserAccessTokenUsingPKCE();throw t}}async getNewUserAccessTokenUsingPKCE(){const e=function(){let e="";for(let t=0;t<44;++t)e+=Math.floor(16*Math.random()).toString(16);return e}(),n=await async function(e){const t=await s(e,{outputFormat:"buffer"});return[...new Uint8Array(t)]}(e),o=(a=n,btoa(String.fromCharCode.apply(null,a)).replace(/\+/g,"-").replace(/\//g,"_").replace(/[=]+$/,""));var a;const i=await this.ajax({url:this.baseUrl+"/oauth2/authorize?"+t.stringify({client_id:this.clientId,client_secret:this.clientSecret,response_type:"code",code_challenge:o,code_challenge_method:"S256",redirect_uri:this.baseUrl}),method:"get",dataType:"text",contentType:u,rawResponse:!0}),c=r.parse(i.url,!0).query.code,l=await this.ajax({url:this.baseUrl+"/oauth2/token",method:"post",dataType:"json",contentType:u,data:{client_id:this.clientId,client_secret:this.clientSecret,grant_type:"authorization_code",redirect_uri:this.baseUrl,code_verifier:e,code:c}}),{access_token:d,refresh_token:p}=l;return this.setStoredCredentials({authType:h,userId:this.userId,accessToken:d,refreshToken:p}),d}async requestAccessToken(){const e=this.getStoredCredentials();return e?e.accessToken:this.getNewAccessToken()}isNewAccessTokenNeeded(e){return 401===e}isUserLoggedOut(e){return 401===e}prepareBody(e,r){switch(r){case p:return JSON.stringify(e);case u:return t.stringify(e);default:return e}}async request(){for(var e=arguments.length,t=new Array(e),r=0;r<e;r++)t[r]=arguments[r];const[s]=t;if("object"!=typeof s)throw new TypeError("Expected an object.");this.validateInstanceConfiguration();try{const e=await this.requestAccessToken(),{headers:t={},url:r}=s;let a=""+this.baseUrl+r,i={};if(this.shouldUseApiMockServer()){var n;Boolean(null==(n=this.apiMockServerUrlsToMock)?void 0:n.some((e=>r.includes(e))))&&(a=(""+this.apiMockServerUrl+r).replace("/ccapi","").replace(/%5B/g,"[").replace(/%5D/g,"]"),i={"X-Api-Key":this.apiMockServerKey})}return await this.ajax(o({contentType:p,dataType:"json"},s,{url:a,headers:o({},t,void 0===t.Authorization&&{Authorization:"Bearer "+e},i)}))}catch(a){if(s.rawResponse)throw a;let e=a.responseText,r=!1;if(a&&a.responseJSON)e=a.responseJSON,r=!0;else try{e=JSON.parse(a.responseText),r=!0}catch(i){e=a.responseText,r=!1}if(this.isNewAccessTokenNeeded(a.status))return await this.getNewAccessToken(),this.request(...t);throw r&&!this.isCcapiErrorResponse(e)&&(e={errors:[o({status:String(a.status),code:e.error,detail:e.error_description},e)]}),e}}shouldUseApiMockServer(){return Boolean(this.apiMockServerUrl)&&Boolean(this.apiMockServerKey)}shouldImpersonateUser(){return Boolean(this.impersonatedUsername)}}var T=function e(){let t;function r(e){return s().request(e)}function s(){if(!t){var e,r;const s=null==(e=window.app)?void 0:e.settings,n=null!=(r=null==s?void 0:s.ccapi)?r:new TypeError("CCAPI configuration is not available.");if(n instanceof TypeError)throw n;t=new g({baseUrl:n.baseUrl,authType:n.authType,clientId:n.clientId,clientSecret:n.clientSecret,userId:s.userId,loggedOutUserAction:()=>(window.location.reload(),Promise.resolve()),apiMockServerUrl:n.apiMockServerUrl,apiMockServerKey:n.apiMockServerKey,apiMockServerUrlsToMock:n.apiMockServerUrlsToMock,impersonatedUsername:n.impersonatedUsername})}return t}return r.getClientInstance=s,r.createNewModule=e,r}();export{T as default};
