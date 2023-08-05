"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var settings_1 = require("../settings");
function startsWith(str, searchString, position) {
    if (position === void 0) { position = 0; }
    return str.substr(position, searchString.length) == searchString;
}
exports.startsWith = startsWith;
function uuid4() {
    // from ipython project
    // http://www.ietf.org/rfc/rfc4122.txt
    var s = new Array(32);
    var hexDigits = "0123456789ABCDEF";
    for (var i = 0; i < 32; i++) {
        s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
    }
    s[12] = "4"; // bits 12-15 of the time_hi_and_version field to 0010
    s[16] = hexDigits.substr((s[16].charCodeAt(0) & 0x3) | 0x8, 1); // bits 6-7 of the clock_seq_hi_and_reserved to 01
    return s.join("");
}
exports.uuid4 = uuid4;
var counter = 1000;
function uniqueId(prefix) {
    var id = settings_1.settings.dev ? "j" + counter++ : uuid4();
    if (prefix != null)
        return prefix + "-" + id;
    else
        return id;
}
exports.uniqueId = uniqueId;
function escape(s) {
    return s.replace(/(?:[&<>"'`])/g, function (ch) {
        switch (ch) {
            case '&': return '&amp;';
            case '<': return '&lt;';
            case '>': return '&gt;';
            case '"': return '&quot;';
            case "'": return '&#x27;';
            case '`': return '&#x60;';
            default: return ch;
        }
    });
}
exports.escape = escape;
function unescape(s) {
    return s.replace(/&(amp|lt|gt|quot|#x27|#x60);/g, function (_, entity) {
        switch (entity) {
            case 'amp': return '&';
            case 'lt': return '<';
            case 'gt': return '>';
            case 'quot': return '"';
            case '#x27': return "'";
            case '#x60': return '`';
            default: return entity;
        }
    });
}
exports.unescape = unescape;
function use_strict(code) {
    return "'use strict';\n" + code;
}
exports.use_strict = use_strict;
