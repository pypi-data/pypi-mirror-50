"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var input_widget_1 = require("./input_widget");
var dom_1 = require("../../core/dom");
var p = require("../../core/properties");
var inputs_1 = require("../../styles/widgets/inputs");
var TextInputView = /** @class */ (function (_super) {
    tslib_1.__extends(TextInputView, _super);
    function TextInputView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TextInputView.prototype.connect_signals = function () {
        var _this = this;
        _super.prototype.connect_signals.call(this);
        this.connect(this.model.properties.name.change, function () { return _this.input_el.name = _this.model.name || ""; });
        this.connect(this.model.properties.value.change, function () { return _this.input_el.value = _this.model.value; });
        this.connect(this.model.properties.value_input.change, function () { return _this.input_el.value = _this.model.value_input; });
        this.connect(this.model.properties.disabled.change, function () { return _this.input_el.disabled = _this.model.disabled; });
        this.connect(this.model.properties.placeholder.change, function () { return _this.input_el.placeholder = _this.model.placeholder; });
    };
    TextInputView.prototype.render = function () {
        var _this = this;
        _super.prototype.render.call(this);
        this.input_el = dom_1.input({
            type: "text",
            class: inputs_1.bk_input,
            name: this.model.name,
            value: this.model.value,
            disabled: this.model.disabled,
            placeholder: this.model.placeholder,
        });
        this.input_el.addEventListener("change", function () { return _this.change_input(); });
        this.input_el.addEventListener("input", function () { return _this.change_input_oninput(); });
        this.group_el.appendChild(this.input_el);
    };
    TextInputView.prototype.change_input = function () {
        this.model.value = this.input_el.value;
        _super.prototype.change_input.call(this);
    };
    TextInputView.prototype.change_input_oninput = function () {
        this.model.value_input = this.input_el.value;
        _super.prototype.change_input.call(this);
    };
    TextInputView.__name__ = "TextInputView";
    return TextInputView;
}(input_widget_1.InputWidgetView));
exports.TextInputView = TextInputView;
var TextInput = /** @class */ (function (_super) {
    tslib_1.__extends(TextInput, _super);
    function TextInput(attrs) {
        return _super.call(this, attrs) || this;
    }
    TextInput.initClass = function () {
        this.prototype.default_view = TextInputView;
        this.define({
            value: [p.String, ""],
            value_input: [p.String, ""],
            placeholder: [p.String, ""],
        });
    };
    TextInput.__name__ = "TextInput";
    return TextInput;
}(input_widget_1.InputWidget));
exports.TextInput = TextInput;
TextInput.initClass();
