import{_ as t}from"./f141f5a29b.js";import{F as e,S as o}from"./825e28468d.js";import a from"./e5795dfffe.js";import"./7abd8ddb57.js";import{t as s}from"./7c6ae762e4.js";import"./2be7671a02.js";import"./a20b5a7092.js";import"./eae60494e1.js";class i extends e{static childrenEl={clearButton:".GeoLocationSelector-iconClose"};static events={"keydown .GeoLocationSelector-autoCompleteInput":"preventSubmit","focus .GeoLocationSelector-autoCompleteInput":"triggerSearchDropdown","blur .GeoLocationSelector-autoCompleteInput":"inputCleanUp","click .GeoLocationSelector-iconClose":"clear"};constructor(t){super(t),this.cacheChildrenEl({input:this.props.input}),this.setState({autoCompleteValue:this.$input.value}),this.store=new o,this.setup()}async setup(){const[{default:e},{debounce:o},{findAll:s}]=await Promise.all([t((()=>import("./01cd71c63d.js")),["01cd71c63d.js","825e28468d.js","2be7671a02.js","f141f5a29b.js","a20b5a7092.js","eae60494e1.js"]),t((()=>import("./4ea6aa4332.js")),[]),t((()=>import("./d2d2a5e5de.js").then((t=>t.i))),["d2d2a5e5de.js","a20b5a7092.js"])]);this.autosuggest=e(this.$input,{htmlClassNamespace:"GeoLocationSelector-dropdown",decorateInputEvent:t=>o(300,t),onOptionSelect:(t,e,o)=>{this.setState({preventSubmit:!0}),this.$input.blur(),o.autoLocate?this.autoLocate():this.setState({disabled:!1,autoCompleteValue:e,autoLocateError:!1,coordinates:{lat:o.latitude,lng:o.longitude}})},onFocus:async t=>""===this.$input.value?this.props.autoLocate?[this.generateAutolocate()]:[]:t,onQueryInput:async t=>{if(t.trim().length<3)return this.prependAutoLocate([]);this.setState({loading:!0});const e=await a({url:this.props.url.replace("{{address}}",t),type:"get"});return this.store.reset(),this.store.sync(e),this.setState({loading:!1}),this.prependAutoLocate(this.store.findAll("locality-suggestion").map((e=>({content:s({searchWords:[t],textToHighlight:e.title}).map((t=>{const{end:o,highlight:a,start:s}=t,i=e.title.substr(s,o-s);return a?`\n\t\t\t\t\t\t\t\t\t\t<mark\n\t\t\t\t\t\t\t\t\t\t\tclass="GeoLocationSelector-dropdown-match"\n\t\t\t\t\t\t\t\t\t\t\t>${i}</mark\n\t\t\t\t\t\t\t\t\t\t>\n\t\t\t\t\t\t\t\t\t`:i})).join(""),value:e.title,meta:e.coordinate}))))}})}preventSubmit(t){if(13===t.keyCode){t.preventDefault();const[e]=this.store.findAll("locality-suggestion");e&&!this.state.preventSubmit&&(this.$input.blur(),this.setState({disabled:!1,autoCompleteValue:e.title,autoLocateError:!1,coordinates:{lat:e.coordinate.latitude,lng:e.coordinate.longitude}}))}this.setState({preventSubmit:!1})}autoLocate(){return this.setState({loading:!0}),this.props.parent.autoLocateSelector.fetch().then((t=>a({url:this.props.autoLocate.url.replace("{{lat}}",t.coords.latitude).replace("{{lng}}",t.coords.longitude)}).then((e=>{const o=e.data.attributes;this.setState({disabled:!1,loading:!1,autoCompleteValue:`${o.street} ${o.houseNumber}, ${o.town}`,coordinates:{lat:t.coords.latitude,lng:t.coords.longitude}})})))).catch((t=>{throw this.setState({loading:!1}),t}))}prependAutoLocate(t){return this.props.autoLocate&&t.unshift(this.generateAutolocate()),t}generateAutolocate(){return{content:`\n\t\t\t\t<button\n\t\t\t\t\ttype="button"\n\t\t\t\t\tclass="button-flat button-flat--alpha button-flat--with-icon button-standard--full GeoLocationSelector-autoLocateButton"\n\t\t\t\t>\n\t\t\t\t\t<i\n\t\t\t\t\t\tclass="icon icon--xs icon--geolocate GeoLocationSelector-iconGeolocate"\n\t\t\t\t\t\taria-hidden="true"\n\t\t\t\t\t\trole="presentation"\n\t\t\t\t\t></i>\n\t\t\t\t\t${s("geolocation.web.filter.autolocate_fetch")}\n\t\t\t\t</button>\n\t\t\t`,value:"",meta:{autoLocate:!0}}}triggerSearchDropdown(t){this.props.isRangeBlocked()&&(t.preventDefault(),this.$input.blur(),this.props.parent.props.onConflict())}inputCleanUp(){this.props.parent.disabled?this.setState({autoCompleteValue:""}):""===this.$input.value?this.clear():this.state.autoCompleteValue!==this.$input.value&&this.setState({autoCompleteValue:this.state.autoCompleteValue})}clear(){this.setState({disabled:!0,autoLocateError:!1,autoCompleteValue:"",coordinates:{lat:"",lng:""}})}render(t,e){"disabled"!==t&&"coordinates"!==t&&"autoLocateError"!==t&&"loading"!==t||this.props.update({[t]:e}),"autoCompleteValue"===t&&(this.$input.value=e),"disabled"===t&&(this.$clearButton.classList.toggle("hidden",e),e&&(this.$input.value=""))}}export{i as default};