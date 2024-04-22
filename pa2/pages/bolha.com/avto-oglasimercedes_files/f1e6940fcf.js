import{F as t}from"./825e28468d.js";import{t as i}from"./d896c9814e.js";import{s as o}from"./436d401516.js";import"./7abd8ddb57.js";import{t as s}from"./7c6ae762e4.js";class n extends t{static el=".notification";static events={"click .notification-action--remove button"(){this.props.handleRemove()}};static propsSchema={isWrapped:{type:Boolean,default:!1},isSolo:{type:Boolean,default:!1},isEnlarged:{type:Boolean,default:!1},isInfo:{type:Boolean,default:!1},isWarning:{type:Boolean,default:!1},isSuccess:{type:Boolean,default:!1},isError:{type:Boolean,default:!1},isRemovable:{type:Boolean,default:!1},message:{type:String,required:!0},handleRemove:{type:Function,default:()=>{}}};static defaultProps={isWrapped:!1,isSolo:!1,isEnlarged:!1,isInfo:!1,isWarning:!1,isSuccess:!1,isError:!1,isRemovable:!1,handleRemove:()=>{}};constructor(t){super(t),this.setState({initialRender:!0})}setElement(){this.$el=i`
			<div
				class="${o({"wrap-notification":this.props.isWrapped,"wrap-notification--solo":this.props.isWrapped&&this.props.isSolo})}"
			>
				<div
					class="${o(["notification",{"notification--enlarged":this.props.isEnlarged,"notification--info":this.props.isInfo,"notification--warning":this.props.isWarning,"notification--success":this.props.isSuccess,"notification--invalid":this.props.isError,"is-removable":this.props.isRemovable}])}"
					role="alert"
				>
					<div class="notification-content">
						<div class="notification-message">
							${this.props.message}
						</div>
						${this.props.isRemovable?`<div class="notification-action notification-action--remove">\n\t\t\t\t<button\n\t\t\t\t\ttype="button"\n\t\t\t\t\tclass="link-standard link-standard--alpha"\n\t\t\t\t>\n\t\t\t\t\t<span>${s("common.notification.close_caption")}</span>\n\t\t\t\t\t<i\n\t\t\t\t\t\tclass="${o(["icon icon--cancel",{"icon--s":this.props.isEnlarged,"icon--s icon--action":!this.props.isEnlarged}])}"\n\t\t\t\t\t\taria-hidden="true"\n\t\t\t\t\t\trole="presentation"\n\t\t\t\t\t></i>\n\t\t\t\t</button>\n\t\t\t</div>`:""}
					</div>
				</div>
			</div>
		`}}export{n as N};
