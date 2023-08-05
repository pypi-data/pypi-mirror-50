"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var input_widget_1 = require("./input_widget");
var dom_1 = require("../../core/dom");
var p = require("../../core/properties");
var Pikaday = require("pikaday");
var inputs_1 = require("../../styles/widgets/inputs");
require("../../styles/widgets/pikaday");
Pikaday.prototype.adjustPosition = function () {
    if (this._o.container)
        return;
    this.el.style.position = 'absolute';
    var field = this._o.trigger;
    var width = this.el.offsetWidth;
    var height = this.el.offsetHeight;
    var viewportWidth = window.innerWidth || document.documentElement.clientWidth;
    var viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    var scrollTop = window.pageYOffset || document.body.scrollTop || document.documentElement.scrollTop;
    var clientRect = field.getBoundingClientRect();
    var left = clientRect.left + window.pageXOffset;
    var top = clientRect.bottom + window.pageYOffset;
    // adjust left/top origin to .bk-root
    left -= this.el.parentElement.offsetLeft;
    top -= this.el.parentElement.offsetTop;
    // default position is bottom & left
    if ((this._o.reposition && left + width > viewportWidth) ||
        (this._o.position.indexOf('right') > -1 && left - width + field.offsetWidth > 0))
        left = left - width + field.offsetWidth;
    if ((this._o.reposition && top + height > viewportHeight + scrollTop) ||
        (this._o.position.indexOf('top') > -1 && top - height - field.offsetHeight > 0))
        top = top - height - field.offsetHeight;
    this.el.style.left = left + 'px';
    this.el.style.top = top + 'px';
};
var DatePickerView = /** @class */ (function (_super) {
    tslib_1.__extends(DatePickerView, _super);
    function DatePickerView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DatePickerView.prototype.connect_signals = function () {
        var _this = this;
        _super.prototype.connect_signals.call(this);
        this.connect(this.model.change, function () { return _this.render(); });
    };
    DatePickerView.prototype.render = function () {
        var _this = this;
        if (this._picker != null)
            this._picker.destroy();
        _super.prototype.render.call(this);
        this.input_el = dom_1.input({ type: "text", class: inputs_1.bk_input, disabled: this.model.disabled });
        this.group_el.appendChild(this.input_el);
        this._picker = new Pikaday({
            field: this.input_el,
            defaultDate: this._unlocal_date(new Date(this.model.value)),
            setDefaultDate: true,
            minDate: this.model.min_date != null ? this._unlocal_date(new Date(this.model.min_date)) : undefined,
            maxDate: this.model.max_date != null ? this._unlocal_date(new Date(this.model.max_date)) : undefined,
            onSelect: function (date) { return _this._on_select(date); },
        });
        this._root_element.appendChild(this._picker.el);
    };
    DatePickerView.prototype._unlocal_date = function (date) {
        // this sucks but the date comes in as a UTC timestamp and pikaday uses Date's local
        // timezone-converted representation. We want the date to be as given by the user
        var datestr = date.toISOString().substr(0, 10);
        var tup = datestr.split('-');
        return new Date(Number(tup[0]), Number(tup[1]) - 1, Number(tup[2]));
    };
    DatePickerView.prototype._on_select = function (date) {
        // Always use toDateString()!
        // toString() breaks the websocket #4965.
        // toISOString() returns the wrong day (IE on day earlier) #7048
        // XXX: this should be handled by the serializer
        this.model.value = date.toDateString();
        this.change_input();
    };
    DatePickerView.__name__ = "DatePickerView";
    return DatePickerView;
}(input_widget_1.InputWidgetView));
exports.DatePickerView = DatePickerView;
var DatePicker = /** @class */ (function (_super) {
    tslib_1.__extends(DatePicker, _super);
    function DatePicker(attrs) {
        return _super.call(this, attrs) || this;
    }
    DatePicker.initClass = function () {
        this.prototype.default_view = DatePickerView;
        this.define({
            // TODO (bev) types
            value: [p.Any, new Date().toDateString()],
            min_date: [p.Any],
            max_date: [p.Any],
        });
    };
    DatePicker.__name__ = "DatePicker";
    return DatePicker;
}(input_widget_1.InputWidget));
exports.DatePicker = DatePicker;
DatePicker.initClass();
