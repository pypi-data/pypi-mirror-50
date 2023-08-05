import { XYGlyph, XYGlyphView, XYGlyphData } from "./xy_glyph";
import { Arrayable, Rect } from "../../core/types";
import { Class } from "../../core/class";
import { Anchor } from "../../core/enums";
import * as p from "../../core/properties";
import { Context2d } from "../../core/util/canvas";
import { SpatialIndex } from "../../core/util/spatial";
export declare type CanvasImage = HTMLImageElement;
export interface ImageURLData extends XYGlyphData {
    _url: Arrayable<string>;
    _angle: Arrayable<number>;
    _w: Arrayable<number>;
    _h: Arrayable<number>;
    _bounds_rect: Rect;
    sx: Arrayable<number>;
    sy: Arrayable<number>;
    sw: Arrayable<number>;
    sh: Arrayable<number>;
    max_w: number;
    max_h: number;
    image: Arrayable<CanvasImage | null>;
}
export interface ImageURLView extends ImageURLData {
}
export declare class ImageURLView extends XYGlyphView {
    model: ImageURL;
    visuals: ImageURL.Visuals;
    protected retries: Arrayable<number>;
    protected _images_rendered: boolean;
    initialize(): void;
    protected _index_data(): SpatialIndex;
    protected _set_data(): void;
    has_finished(): boolean;
    protected _map_data(): void;
    protected _render(ctx: Context2d, indices: number[], { image, sx, sy, sw, sh, _angle }: ImageURLData): void;
    protected _final_sx_sy(anchor: Anchor, sx: number, sy: number, sw: number, sh: number): [number, number];
    protected _render_image(ctx: Context2d, i: number, image: CanvasImage, sx: Arrayable<number>, sy: Arrayable<number>, sw: Arrayable<number>, sh: Arrayable<number>, angle: Arrayable<number>): void;
    bounds(): Rect;
}
export declare namespace ImageURL {
    type Attrs = p.AttrsOf<Props>;
    type Props = XYGlyph.Props & {
        url: p.StringSpec;
        anchor: p.Property<Anchor>;
        global_alpha: p.Property<number>;
        angle: p.AngleSpec;
        w: p.DistanceSpec;
        h: p.DistanceSpec;
        dilate: p.Property<boolean>;
        retry_attempts: p.Property<number>;
        retry_timeout: p.Property<number>;
    };
    type Visuals = XYGlyph.Visuals;
}
export interface ImageURL extends ImageURL.Attrs {
}
export declare class ImageURL extends XYGlyph {
    properties: ImageURL.Props;
    default_view: Class<ImageURLView>;
    constructor(attrs?: Partial<ImageURL.Attrs>);
    static initClass(): void;
}
