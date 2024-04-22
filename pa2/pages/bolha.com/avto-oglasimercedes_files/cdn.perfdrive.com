<html><head><title>Google CDN</title></head><body>
<style>
body {
  font-family: monospace;
}
ul {
    list-style-type: none;
}
.property {
  font-weight: bold;
}
.type-number {
  color: blue;
}
.type-string {
  color: green;
}
</style><div>{<ul><li><div><span class="property">resource</span>: <span class="type-string">"Google CDN"</span>,</div></li>
    <li><div><span class="property">message</span>: <span class="type-string">"invalid path"</span>,</div></li>
    <li><div><span class="property">code</span>: <span class="type-number">403</span></div></li></ul>}</div></body></html>
