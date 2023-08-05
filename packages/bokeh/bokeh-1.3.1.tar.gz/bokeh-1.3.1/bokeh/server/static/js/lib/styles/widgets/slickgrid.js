"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
require("../root");
var _a = require("../../core/dom");
_a.styles.append(".bk-root {\n  /*\nIMPORTANT:\nIn order to preserve the uniform grid appearance, all cell styles need to have padding, margin and border sizes.\nNo built-in (selected, editable, highlight, flashing, invalid, loading, :focus) or user-specified CSS\nclasses should alter those!\n*/\n  /*\nIMPORTANT:\nIn order to preserve the uniform grid appearance, all cell styles need to have padding, margin and border sizes.\nNo built-in (selected, editable, highlight, flashing, invalid, loading, :focus) or user-specified CSS\nclasses should alter those!\n*/\n  /* Menu button */\n  /* Menu */\n  /* Menu items */\n  /* Disabled */\n}\n.bk-root .slick-header.ui-state-default,\n.bk-root .slick-headerrow.ui-state-default,\n.bk-root .slick-footerrow.ui-state-default,\n.bk-root .slick-top-panel-scroller.ui-state-default {\n  width: 100%;\n  overflow: auto;\n  position: relative;\n  border-left: 0px !important;\n}\n.bk-root .slick-header.ui-state-default {\n  overflow: inherit;\n}\n.bk-root .slick-header::-webkit-scrollbar,\n.bk-root .slick-headerrow::-webkit-scrollbar,\n.bk-root .slick-footerrow::-webkit-scrollbar {\n  display: none;\n}\n.bk-root .slick-header-columns,\n.bk-root .slick-headerrow-columns,\n.bk-root .slick-footerrow-columns {\n  position: relative;\n  white-space: nowrap;\n  cursor: default;\n  overflow: hidden;\n}\n.bk-root .slick-header-column.ui-state-default {\n  position: relative;\n  display: inline-block;\n  box-sizing: content-box !important;\n  /* this here only for Firefox! */\n  overflow: hidden;\n  -o-text-overflow: ellipsis;\n  text-overflow: ellipsis;\n  height: 16px;\n  line-height: 16px;\n  margin: 0;\n  padding: 4px;\n  border-right: 1px solid silver;\n  border-left: 0px !important;\n  border-top: 0px !important;\n  border-bottom: 0px !important;\n  float: left;\n}\n.bk-root .slick-headerrow-column.ui-state-default,\n.bk-root .slick-footerrow-column.ui-state-default {\n  padding: 4px;\n}\n.bk-root .slick-header-column-sorted {\n  font-style: italic;\n}\n.bk-root .slick-sort-indicator {\n  display: inline-block;\n  width: 8px;\n  height: 5px;\n  margin-left: 4px;\n  margin-top: 6px;\n  float: left;\n}\n.bk-root .slick-sort-indicator-numbered {\n  display: inline-block;\n  width: 8px;\n  height: 5px;\n  margin-left: 4px;\n  margin-top: 0;\n  line-height: 20px;\n  float: left;\n  font-family: Arial;\n  font-style: normal;\n  font-weight: bold;\n  color: #6190CD;\n}\n.bk-root .slick-sort-indicator-desc {\n  background: url(images/sort-desc.gif);\n}\n.bk-root .slick-sort-indicator-asc {\n  background: url(images/sort-asc.gif);\n}\n.bk-root .slick-resizable-handle {\n  position: absolute;\n  font-size: 0.1px;\n  display: block;\n  cursor: col-resize;\n  width: 9px;\n  right: -5px;\n  top: 0;\n  height: 100%;\n  z-index: 1;\n}\n.bk-root .slick-sortable-placeholder {\n  background: silver;\n}\n.bk-root .grid-canvas {\n  position: relative;\n  outline: 0;\n}\n.bk-root .slick-row.ui-widget-content,\n.bk-root .slick-row.ui-state-active {\n  position: absolute;\n  border: 0px;\n  width: 100%;\n}\n.bk-root .slick-cell,\n.bk-root .slick-headerrow-column,\n.bk-root .slick-footerrow-column {\n  position: absolute;\n  border: 1px solid transparent;\n  border-right: 1px dotted silver;\n  border-bottom-color: silver;\n  overflow: hidden;\n  -o-text-overflow: ellipsis;\n  text-overflow: ellipsis;\n  vertical-align: middle;\n  z-index: 1;\n  padding: 1px 2px 2px 1px;\n  margin: 0;\n  white-space: nowrap;\n  cursor: default;\n}\n.bk-root .slick-cell,\n.bk-root .slick-headerrow-column {\n  border-bottom-color: silver;\n}\n.bk-root .slick-footerrow-column {\n  border-top-color: silver;\n}\n.bk-root .slick-group-toggle {\n  display: inline-block;\n}\n.bk-root .slick-cell.highlighted {\n  background: lightskyblue;\n  background: rgba(0, 0, 255, 0.2);\n  -webkit-transition: all 0.5s;\n  -moz-transition: all 0.5s;\n  -o-transition: all 0.5s;\n  transition: all 0.5s;\n}\n.bk-root .slick-cell.flashing {\n  border: 1px solid red !important;\n}\n.bk-root .slick-cell.editable {\n  z-index: 11;\n  overflow: visible;\n  background: white;\n  border-color: black;\n  border-style: solid;\n}\n.bk-root .slick-cell:focus {\n  outline: none;\n}\n.bk-root .slick-reorder-proxy {\n  display: inline-block;\n  background: blue;\n  opacity: 0.15;\n  cursor: move;\n}\n.bk-root .slick-reorder-guide {\n  display: inline-block;\n  height: 2px;\n  background: blue;\n  opacity: 0.7;\n}\n.bk-root .slick-selection {\n  z-index: 10;\n  position: absolute;\n  border: 2px dashed black;\n}\n.bk-root .slick-header-columns {\n  background: url('images/header-columns-bg.gif') repeat-x center bottom;\n  border-bottom: 1px solid silver;\n}\n.bk-root .slick-header-column {\n  background: url('images/header-columns-bg.gif') repeat-x center bottom;\n  border-right: 1px solid silver;\n}\n.bk-root .slick-header-column:hover,\n.bk-root .slick-header-column-active {\n  background: white url('images/header-columns-over-bg.gif') repeat-x center bottom;\n}\n.bk-root .slick-headerrow {\n  background: #fafafa;\n}\n.bk-root .slick-headerrow-column {\n  background: #fafafa;\n  border-bottom: 0;\n  height: 100%;\n}\n.bk-root .slick-row.ui-state-active {\n  background: #F5F7D7;\n}\n.bk-root .slick-row {\n  position: absolute;\n  background: white;\n  border: 0px;\n  line-height: 20px;\n}\n.bk-root .slick-row.selected {\n  z-index: 10;\n  background: #DFE8F6;\n}\n.bk-root .slick-cell {\n  padding-left: 4px;\n  padding-right: 4px;\n}\n.bk-root .slick-group {\n  border-bottom: 2px solid silver;\n}\n.bk-root .slick-group-toggle {\n  width: 9px;\n  height: 9px;\n  margin-right: 5px;\n}\n.bk-root .slick-group-toggle.expanded {\n  background: url(images/collapse.gif) no-repeat center center;\n}\n.bk-root .slick-group-toggle.collapsed {\n  background: url(images/expand.gif) no-repeat center center;\n}\n.bk-root .slick-group-totals {\n  color: gray;\n  background: white;\n}\n.bk-root .slick-group-select-checkbox {\n  width: 13px;\n  height: 13px;\n  margin: 3px 10px 0 0;\n  display: inline-block;\n}\n.bk-root .slick-group-select-checkbox.checked {\n  background: url(images/GrpCheckboxY.png) no-repeat center center;\n}\n.bk-root .slick-group-select-checkbox.unchecked {\n  background: url(images/GrpCheckboxN.png) no-repeat center center;\n}\n.bk-root .slick-cell.selected {\n  background-color: beige;\n}\n.bk-root .slick-cell.active {\n  border-color: gray;\n  border-style: solid;\n}\n.bk-root .slick-sortable-placeholder {\n  background: silver !important;\n}\n.bk-root .slick-row.odd {\n  background: #fafafa;\n}\n.bk-root .slick-row.ui-state-active {\n  background: #F5F7D7;\n}\n.bk-root .slick-row.loading {\n  opacity: 0.5;\n}\n.bk-root .slick-cell.invalid {\n  border-color: red;\n  -moz-animation-duration: 0.2s;\n  -webkit-animation-duration: 0.2s;\n  -moz-animation-name: slickgrid-invalid-hilite;\n  -webkit-animation-name: slickgrid-invalid-hilite;\n}\n@-moz-keyframes slickgrid-invalid-hilite {\n  from {\n    box-shadow: 0 0 6px red;\n  }\n  to {\n    box-shadow: none;\n  }\n}\n@-webkit-keyframes slickgrid-invalid-hilite {\n  from {\n    box-shadow: 0 0 6px red;\n  }\n  to {\n    box-shadow: none;\n  }\n}\n.bk-root .slick-column-name,\n.bk-root .slick-sort-indicator {\n  /**\n   * This makes all \"float:right\" elements after it that spill over to the next line\n   * display way below the lower boundary of the column thus hiding them.\n   */\n  display: inline-block;\n  float: left;\n  margin-bottom: 100px;\n}\n.bk-root .slick-header-button {\n  display: inline-block;\n  float: right;\n  vertical-align: top;\n  margin: 1px;\n  /**\n  * This makes all \"float:right\" elements after it that spill over to the next line\n  * display way below the lower boundary of the column thus hiding them.\n  */\n  margin-bottom: 100px;\n  height: 15px;\n  width: 15px;\n  background-repeat: no-repeat;\n  background-position: center center;\n  cursor: pointer;\n}\n.bk-root .slick-header-button-hidden {\n  width: 0;\n  -webkit-transition: 0.2s width;\n  -ms-transition: 0.2s width;\n  transition: 0.2s width;\n}\n.bk-root .slick-header-column:hover > .slick-header-button {\n  width: 15px;\n}\n.bk-root .slick-header-menubutton {\n  position: absolute;\n  right: 0;\n  top: 0;\n  bottom: 0;\n  width: 14px;\n  background-repeat: no-repeat;\n  background-position: left center;\n  background-image: url(../images/down.gif);\n  cursor: pointer;\n  display: none;\n  border-left: thin ridge silver;\n}\n.bk-root .slick-header-column:hover > .slick-header-menubutton,\n.bk-root .slick-header-column-active .slick-header-menubutton {\n  display: inline-block;\n}\n.bk-root .slick-header-menu {\n  position: absolute;\n  display: inline-block;\n  margin: 0;\n  padding: 2px;\n  cursor: default;\n}\n.bk-root .slick-header-menuitem {\n  list-style: none;\n  margin: 0;\n  padding: 0;\n  cursor: pointer;\n}\n.bk-root .slick-header-menuicon {\n  display: inline-block;\n  width: 16px;\n  height: 16px;\n  vertical-align: middle;\n  margin-right: 4px;\n  background-repeat: no-repeat;\n  background-position: center center;\n}\n.bk-root .slick-header-menucontent {\n  display: inline-block;\n  vertical-align: middle;\n}\n.bk-root .slick-header-menuitem-disabled {\n  color: silver;\n}\n.bk-root .slick-columnpicker {\n  border: 1px solid #718BB7;\n  background: #f0f0f0;\n  padding: 6px;\n  -moz-box-shadow: 2px 2px 2px silver;\n  -webkit-box-shadow: 2px 2px 2px silver;\n  box-shadow: 2px 2px 2px silver;\n  min-width: 150px;\n  cursor: default;\n  position: absolute;\n  z-index: 20;\n  overflow: auto;\n  resize: both;\n}\n.bk-root .slick-columnpicker > .close {\n  float: right;\n}\n.bk-root .slick-columnpicker .title {\n  font-size: 16px;\n  width: 60%;\n  border-bottom: solid 1px #d6d6d6;\n  margin-bottom: 10px;\n}\n.bk-root .slick-columnpicker li {\n  list-style: none;\n  margin: 0;\n  padding: 0;\n  background: none;\n}\n.bk-root .slick-columnpicker input {\n  margin: 4px;\n}\n.bk-root .slick-columnpicker li a {\n  display: block;\n  padding: 4px;\n  font-weight: bold;\n}\n.bk-root .slick-columnpicker li a:hover {\n  background: white;\n}\n.bk-root .slick-pager {\n  width: 100%;\n  height: 26px;\n  border: 1px solid gray;\n  border-top: 0;\n  background: url('../images/header-columns-bg.gif') repeat-x center bottom;\n  vertical-align: middle;\n}\n.bk-root .slick-pager .slick-pager-status {\n  display: inline-block;\n  padding: 6px;\n}\n.bk-root .slick-pager .ui-icon-container {\n  display: inline-block;\n  margin: 2px;\n  border-color: gray;\n}\n.bk-root .slick-pager .slick-pager-nav {\n  display: inline-block;\n  float: left;\n  padding: 2px;\n}\n.bk-root .slick-pager .slick-pager-settings {\n  display: block;\n  float: right;\n  padding: 2px;\n}\n.bk-root .slick-pager .slick-pager-settings * {\n  vertical-align: middle;\n}\n.bk-root .slick-pager .slick-pager-settings a {\n  padding: 2px;\n  text-decoration: underline;\n  cursor: pointer;\n}\n.bk-root .slick-header-columns {\n  background-image: url(\"data:image/gif;base64,R0lGODlhAgAYAIcAANDQ0Ovs7uzt7+3u8O7v8e/w8vDx8/Hy9Pn5+QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAAAAP8ALAAAAAACABgAAAghABEIHEiwYMEDCA8YWMiwgMMCBAgMmDhAgIAAGAMAABAQADs=\");\n}\n.bk-root .slick-header-column {\n  background-image: url(\"data:image/gif;base64,R0lGODlhAgAYAIcAANDQ0Ovs7uzt7+3u8O7v8e/w8vDx8/Hy9Pn5+QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAAAAP8ALAAAAAACABgAAAghABEIHEiwYMEDCA8YWMiwgMMCBAgMmDhAgIAAGAMAABAQADs=\");\n}\n.bk-root .slick-header-column:hover,\n.bk-root .slick-header-column-active {\n  background-image: url(\"data:image/gif;base64,R0lGODlhAgAWAIcAAKrM9tno++vz/QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAAAAP8ALAAAAAACABYAAAgUAAUIHEiwoIAACBMqXMhwIQAAAQEAOw==\");\n}\n.bk-root .slick-group-toggle.expanded {\n  background-image: url(\"data:image/gif;base64,R0lGODlhCQAJAPcAAAFGeoCAgNXz/+v5/+v6/+z5/+36//L7//X8//j9/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAACQAJAAAIMwADCBxIUIDBgwIEChgwwECBAgQUFjBAkaJCABgxGlB4AGHCAAIQiBypEEECkScJqgwQEAA7\");\n}\n.bk-root .slick-group-toggle.collapsed {\n  background-image: url(\"data:image/gif;base64,R0lGODlhCQAJAPcAAAFGeoCAgNXz/+v5/+v6/+z5/+36//L7//X8//j9/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAACQAJAAAIOAADCBxIUIDBgwIEChgwAECBAgQUFjAAQIABAwoBaNSIMYCAAwIqGlSIAEHFkiQTIBCgkqDLAAEBADs=\");\n}\n.bk-root .slick-group-select-checkbox.checked {\n  background-image: url(\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAIAAACQKrqGAAAABGdBTUEAALGPC/xhBQAAAAlwSFlzAAAOwQAADsEBuJFr7QAAABl0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xNkRpr/UAAAEcSURBVChTjdI9S8NQFAbg/raQXVwCRRFE7GK7OXTwD+ikk066VF3a0ja0hQTyQdJrwNq0zrYSQRLEXMSWSlCIb8glqRcFD+9yz3nugXwU4n9XQqMoGjj36uBJsTwuaNo3EwBG4Yy7pe7Gv8YcvhJCGFVsjxsjxujj6OTSGlHv+U2WZUZbPWKOv1ZjT5a7pbIoiptbO5b73mwrjHa1B27l8VlTEIS1damlTnEE+EEN9/P8WrfH81qdAIGeXvTTmzltdCy46sEhxpKUINReZR9NnqZbr9puugxV3NjWh/k74WmmEdWhmUNy2jNmWRc6fZTVADCqao52u+DGWTACYNT3fRxwtatPufTNR4yCIGAUn5hS+vJHhWGY/ANx/A3tvdv+1tZmuwAAAABJRU5ErkJggg==\");\n}\n.bk-root .slick-group-select-checkbox.unchecked {\n  background-image: url(\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAIAAACQKrqGAAAABGdBTUEAALGPC/xhBQAAAAlwSFlzAAAOwQAADsEBuJFr7QAAABl0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xNkRpr/UAAACXSURBVChT1dIxC4MwEAXg/v8/VOhQVDBNakV0KA6pxS4JhWRSIYPEJxwdDi1de7wleR+3JIf486w0hKCKRpSvvOhZcCmvNQBRuKqdah03U7UjNNH81rOaBYDo8SQaPX8JANFEaLaGBeAPaaY61rGksiN6TmR5H1j9CSoAosYYHLA7vTxYMvVEZa0liif23r93xjm3/oEYF8PiDn/I2FHCAAAAAElFTkSuQmCC\");\n}\n.bk-root .slick-sort-indicator-desc {\n  background-image: url(\"data:image/gif;base64,R0lGODlhDQAFAIcAAGGQzUD/QOPu+wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAMAAAEALAAAAAANAAUAAAgeAAUAGEgQgIAACBEKLHgwYcKFBh1KFNhQosOKEgMCADs=\");\n}\n.bk-root .slick-sort-indicator-asc {\n  background-image: url(\"data:image/gif;base64,R0lGODlhDQAFAIcAAGGQzUD/QOPu+wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAMAAAEALAAAAAANAAUAAAgbAAMIDABgoEGDABIeRJhQ4cKGEA8KmEiRosGAADs=\");\n}\n.bk-root .slick-header-menubutton {\n  background-image: url(\"data:image/gif;base64,R0lGODlhDgAOAIABADtKYwAAACH5BAEAAAEALAAAAAAOAA4AAAISjI+py+0PHZgUsGobhTn6DxoFADs=\");\n}\n.bk-root .slick-pager {\n  background-image: url(\"data:image/gif;base64,R0lGODlhAgAYAIcAANDQ0Ovs7uzt7+3u8O7v8e/w8vDx8/Hy9Pn5+QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAAAAP8ALAAAAAACABgAAAghABEIHEiwYMEDCA8YWMiwgMMCBAgMmDhAgIAAGAMAABAQADs=\");\n}\n");
