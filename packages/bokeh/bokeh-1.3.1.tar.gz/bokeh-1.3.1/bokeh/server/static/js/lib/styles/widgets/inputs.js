"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
require("../root");
var _a = require("../../core/dom");
_a.styles.append(".bk-root .bk-input {\n  display: inline-block;\n  width: 100%;\n  flex-grow: 1;\n  -webkit-flex-grow: 1;\n  min-height: 31px;\n  padding: 0 12px;\n  background-color: #fff;\n  border: 1px solid #ccc;\n  border-radius: 4px;\n}\n.bk-root .bk-input:focus {\n  border-color: #66afe9;\n  outline: 0;\n  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(102, 175, 233, 0.6);\n}\n.bk-root .bk-input::placeholder,\n.bk-root .bk-input:-ms-input-placeholder,\n.bk-root .bk-input::-moz-placeholder,\n.bk-root .bk-input::-webkit-input-placeholder {\n  color: #999;\n  opacity: 1;\n}\n.bk-root .bk-input[disabled],\n.bk-root .bk-input[readonly] {\n  cursor: not-allowed;\n  background-color: #eee;\n  opacity: 1;\n}\n.bk-root select[multiple].bk-input,\n.bk-root select[size].bk-input,\n.bk-root textarea.bk-input {\n  height: auto;\n}\n.bk-root .bk-input-group {\n  width: 100%;\n  height: 100%;\n  display: inline-flex;\n  display: -webkit-inline-flex;\n  flex-wrap: nowrap;\n  -webkit-flex-wrap: nowrap;\n  align-items: start;\n  -webkit-align-items: start;\n  flex-direction: column;\n  -webkit-flex-direction: column;\n  white-space: nowrap;\n}\n.bk-root .bk-input-group.bk-inline {\n  flex-direction: row;\n  -webkit-flex-direction: row;\n}\n.bk-root .bk-input-group.bk-inline > *:not(:first-child) {\n  margin-left: 5px;\n}\n.bk-root .bk-input-group input[type=\"checkbox\"] + span,\n.bk-root .bk-input-group input[type=\"radio\"] + span {\n  position: relative;\n  top: -2px;\n  margin-left: 3px;\n}\n");
exports.bk_input = "bk-input";
exports.bk_input_group = "bk-input-group";
