"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var models_1 = require("./models");
function or_else(value, default_value) {
    if (value === undefined)
        return default_value;
    else
        return value;
}
function gridplot(children, opts) {
    if (opts === void 0) { opts = {}; }
    var toolbar_location = or_else(opts.toolbar_location, "above");
    var merge_tools = or_else(opts.merge_tools, true);
    var sizing_mode = or_else(opts.sizing_mode, null);
    var tools = [];
    var items = [];
    for (var y = 0; y < children.length; y++) {
        var row = children[y];
        for (var x = 0; x < row.length; x++) {
            var item = row[x];
            if (item == null)
                continue;
            else {
                if (item instanceof models_1.Plot) { // XXX: semantics differ
                    if (merge_tools) {
                        tools.push.apply(tools, item.toolbar.tools);
                        item.toolbar_location = null;
                    }
                    if (opts.plot_width != null)
                        item.plot_width = opts.plot_width;
                    if (opts.plot_height != null)
                        item.plot_height = opts.plot_height;
                }
                items.push([item, y, x]);
            }
        }
    }
    if (!merge_tools || toolbar_location == null)
        return new models_1.GridBox({ children: items, sizing_mode: sizing_mode });
    var grid = new models_1.GridBox({ children: items, sizing_mode: sizing_mode });
    var toolbar = new models_1.ToolbarBox({
        toolbar: new models_1.ProxyToolbar({ tools: tools }),
        toolbar_location: toolbar_location,
    });
    switch (toolbar_location) {
        case "above":
            return new models_1.Column({ children: [toolbar, grid], sizing_mode: sizing_mode });
        case "below":
            return new models_1.Column({ children: [grid, toolbar], sizing_mode: sizing_mode });
        case "left":
            return new models_1.Row({ children: [toolbar, grid], sizing_mode: sizing_mode });
        case "right":
            return new models_1.Row({ children: [grid, toolbar], sizing_mode: sizing_mode });
        default:
            throw new Error("unexpected");
    }
}
exports.gridplot = gridplot;
