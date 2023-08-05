import { Marker } from "./marker";
import { MarkerType } from "../../core/enums";
import { Class } from "../../core/class";
import { Line, Fill } from "../../core/visuals";
import { Context2d } from "../../core/util/canvas";
export declare type RenderOne = (ctx: Context2d, i: number, r: number, line: Line, fill: Fill) => void;
export declare const Asterisk: Class<Marker, any[]>;
export declare const CircleCross: Class<Marker, any[]>;
export declare const CircleX: Class<Marker, any[]>;
export declare const Cross: Class<Marker, any[]>;
export declare const Dash: Class<Marker, any[]>;
export declare const Diamond: Class<Marker, any[]>;
export declare const DiamondCross: Class<Marker, any[]>;
export declare const Hex: Class<Marker, any[]>;
export declare const InvertedTriangle: Class<Marker, any[]>;
export declare const Square: Class<Marker, any[]>;
export declare const SquareCross: Class<Marker, any[]>;
export declare const SquareX: Class<Marker, any[]>;
export declare const Triangle: Class<Marker, any[]>;
export declare const X: Class<Marker, any[]>;
export declare const marker_funcs: {
    [key in MarkerType]: RenderOne;
};
