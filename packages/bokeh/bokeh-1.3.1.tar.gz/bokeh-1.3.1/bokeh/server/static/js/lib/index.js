"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
require("./polyfill");
var version_1 = require("./version");
exports.version = version_1.version;
var embed = require("./embed");
exports.embed = embed;
var embed_1 = require("./embed");
exports.index = embed_1.index;
var protocol = require("./protocol");
exports.protocol = protocol;
var _testing = require("./testing");
exports._testing = _testing;
var logging_1 = require("./core/logging");
exports.logger = logging_1.logger;
exports.set_log_level = logging_1.set_log_level;
var settings_1 = require("./core/settings");
exports.settings = settings_1.settings;
var base_1 = require("./base");
exports.Models = base_1.Models;
var document_1 = require("./document");
exports.documents = document_1.documents;
var safely_1 = require("./safely");
exports.safely = safely_1.safely;
