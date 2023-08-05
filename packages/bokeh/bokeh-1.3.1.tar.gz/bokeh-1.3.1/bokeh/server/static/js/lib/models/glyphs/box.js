"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var spatial_1 = require("../../core/util/spatial");
var glyph_1 = require("./glyph");
var utils_1 = require("./utils");
var hittest = require("../../core/hittest");
var BoxView = /** @class */ (function (_super) {
    tslib_1.__extends(BoxView, _super);
    function BoxView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    BoxView.prototype.get_anchor_point = function (anchor, i, _spt) {
        var left = Math.min(this.sleft[i], this.sright[i]);
        var right = Math.max(this.sright[i], this.sleft[i]);
        var top = Math.min(this.stop[i], this.sbottom[i]); // screen coordinates !!!
        var bottom = Math.max(this.sbottom[i], this.stop[i]); //
        switch (anchor) {
            case "top_left": return { x: left, y: top };
            case "top_center": return { x: (left + right) / 2, y: top };
            case "top_right": return { x: right, y: top };
            case "bottom_left": return { x: left, y: bottom };
            case "bottom_center": return { x: (left + right) / 2, y: bottom };
            case "bottom_right": return { x: right, y: bottom };
            case "center_left": return { x: left, y: (top + bottom) / 2 };
            case "center": return { x: (left + right) / 2, y: (top + bottom) / 2 };
            case "center_right": return { x: right, y: (top + bottom) / 2 };
            default: return null;
        }
    };
    BoxView.prototype._index_box = function (len) {
        var points = [];
        for (var i = 0; i < len; i++) {
            var _a = this._lrtb(i), l = _a[0], r = _a[1], t = _a[2], b = _a[3];
            if (isNaN(l + r + t + b) || !isFinite(l + r + t + b))
                continue;
            points.push({
                x0: Math.min(l, r),
                y0: Math.min(t, b),
                x1: Math.max(r, l),
                y1: Math.max(t, b),
                i: i,
            });
        }
        return new spatial_1.SpatialIndex(points);
    };
    BoxView.prototype._render = function (ctx, indices, _a) {
        var _this = this;
        var sleft = _a.sleft, sright = _a.sright, stop = _a.stop, sbottom = _a.sbottom;
        var _loop_1 = function (i) {
            if (isNaN(sleft[i] + stop[i] + sright[i] + sbottom[i]))
                return "continue";
            ctx.rect(sleft[i], stop[i], sright[i] - sleft[i], sbottom[i] - stop[i]);
            if (this_1.visuals.fill.doit) {
                this_1.visuals.fill.set_vectorize(ctx, i);
                ctx.beginPath();
                ctx.rect(sleft[i], stop[i], sright[i] - sleft[i], sbottom[i] - stop[i]);
                ctx.fill();
            }
            this_1.visuals.hatch.doit2(ctx, i, function () {
                ctx.beginPath();
                ctx.rect(sleft[i], stop[i], sright[i] - sleft[i], sbottom[i] - stop[i]);
                ctx.fill();
            }, function () { return _this.renderer.request_render(); });
            if (this_1.visuals.line.doit) {
                this_1.visuals.line.set_vectorize(ctx, i);
                ctx.beginPath();
                ctx.rect(sleft[i], stop[i], sright[i] - sleft[i], sbottom[i] - stop[i]);
                ctx.stroke();
            }
        };
        var this_1 = this;
        for (var _i = 0, indices_1 = indices; _i < indices_1.length; _i++) {
            var i = indices_1[_i];
            _loop_1(i);
        }
    };
    // We need to clamp the endpoints inside the viewport, because various browser canvas
    // implementations have issues drawing rects with enpoints far outside the viewport
    BoxView.prototype._clamp_viewport = function () {
        var hr = this.renderer.plot_view.frame.bbox.h_range;
        var vr = this.renderer.plot_view.frame.bbox.v_range;
        var n = this.stop.length;
        for (var i = 0; i < n; i++) {
            this.stop[i] = Math.max(this.stop[i], vr.start);
            this.sbottom[i] = Math.min(this.sbottom[i], vr.end);
            this.sleft[i] = Math.max(this.sleft[i], hr.start);
            this.sright[i] = Math.min(this.sright[i], hr.end);
        }
    };
    BoxView.prototype._hit_rect = function (geometry) {
        return this._hit_rect_against_index(geometry);
    };
    BoxView.prototype._hit_point = function (geometry) {
        var sx = geometry.sx, sy = geometry.sy;
        var x = this.renderer.xscale.invert(sx);
        var y = this.renderer.yscale.invert(sy);
        var hits = this.index.indices({ x0: x, y0: y, x1: x, y1: y });
        var result = hittest.create_empty_hit_test_result();
        result.indices = hits;
        return result;
    };
    BoxView.prototype._hit_span = function (geometry) {
        var sx = geometry.sx, sy = geometry.sy;
        var hits;
        if (geometry.direction == 'v') {
            var y = this.renderer.yscale.invert(sy);
            var hr = this.renderer.plot_view.frame.bbox.h_range;
            var _a = this.renderer.xscale.r_invert(hr.start, hr.end), x0 = _a[0], x1 = _a[1];
            hits = this.index.indices({ x0: x0, y0: y, x1: x1, y1: y });
        }
        else {
            var x = this.renderer.xscale.invert(sx);
            var vr = this.renderer.plot_view.frame.bbox.v_range;
            var _b = this.renderer.yscale.r_invert(vr.start, vr.end), y0 = _b[0], y1 = _b[1];
            hits = this.index.indices({ x0: x, y0: y0, x1: x, y1: y1 });
        }
        var result = hittest.create_empty_hit_test_result();
        result.indices = hits;
        return result;
    };
    BoxView.prototype.draw_legend_for_index = function (ctx, bbox, index) {
        utils_1.generic_area_legend(this.visuals, ctx, bbox, index);
    };
    BoxView.__name__ = "BoxView";
    return BoxView;
}(glyph_1.GlyphView));
exports.BoxView = BoxView;
var Box = /** @class */ (function (_super) {
    tslib_1.__extends(Box, _super);
    function Box(attrs) {
        return _super.call(this, attrs) || this;
    }
    Box.initClass = function () {
        this.mixins(['line', 'fill', 'hatch']);
    };
    Box.__name__ = "Box";
    return Box;
}(glyph_1.Glyph));
exports.Box = Box;
Box.initClass();
