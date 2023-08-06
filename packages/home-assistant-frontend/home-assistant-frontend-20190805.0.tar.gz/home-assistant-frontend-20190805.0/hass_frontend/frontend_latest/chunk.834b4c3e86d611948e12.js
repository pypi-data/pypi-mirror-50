(window.webpackJsonp=window.webpackJsonp||[]).push([[95],{664:function(e,a,l){"use strict";l.r(a);l(145);var t=l(3),o=l(25);l(126),l(92);customElements.define("ha-panel-iframe",class extends o.a{static get template(){return t.a`
      <style include="ha-style">
        iframe {
          border: 0;
          width: 100%;
          height: calc(100% - 64px);
        }
      </style>
      <app-toolbar>
        <ha-menu-button hass="[[hass]]" narrow="[[narrow]]"></ha-menu-button>
        <div main-title>[[panel.title]]</div>
      </app-toolbar>

      <iframe
        src="[[panel.config.url]]"
        sandbox="allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
      ></iframe>
    `}static get properties(){return{hass:Object,narrow:Boolean,panel:Object}}})}}]);
//# sourceMappingURL=chunk.834b4c3e86d611948e12.js.map