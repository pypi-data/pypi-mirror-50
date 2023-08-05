import { LineVector, FillVector, HatchVector } from "../../core/property_mixins";
import { Arrayable, Rect } from "../../core/types";
import { Anchor } from "../../core/enums";
import { Line, Fill, Hatch } from "../../core/visuals";
import { SpatialIndex } from "../../core/util/spatial";
import { Context2d } from "../../core/util/canvas";
import { Glyph, GlyphView, GlyphData } from "./glyph";
import { PointGeometry, SpanGeometry, RectGeometry } from "../../core/geometry";
import { Selection } from "../selections/selection";
import * as p from "../../core/properties";
export interface BoxData extends GlyphData {
    _right: Arrayable<number>;
    _bottom: Arrayable<number>;
    _left: Arrayable<number>;
    _top: Arrayable<number>;
    sright: Arrayable<number>;
    sbottom: Arrayable<number>;
    sleft: Arrayable<number>;
    stop: Arrayable<number>;
}
export interface BoxView extends BoxData {
}
export declare abstract class BoxView extends GlyphView {
    model: Box;
    visuals: Box.Visuals;
    get_anchor_point(anchor: Anchor, i: number, _spt: [number, number]): {
        x: number;
        y: number;
    } | null;
    protected abstract _lrtb(i: number): [number, number, number, number];
    protected _index_box(len: number): SpatialIndex;
    protected _render(ctx: Context2d, indices: number[], { sleft, sright, stop, sbottom }: BoxData): void;
    protected _clamp_viewport(): void;
    protected _hit_rect(geometry: RectGeometry): Selection;
    protected _hit_point(geometry: PointGeometry): Selection;
    protected _hit_span(geometry: SpanGeometry): Selection;
    draw_legend_for_index(ctx: Context2d, bbox: Rect, index: number): void;
}
export declare namespace Box {
    type Attrs = p.AttrsOf<Props>;
    type Props = Glyph.Props & LineVector & FillVector & HatchVector;
    type Visuals = Glyph.Visuals & {
        line: Line;
        fill: Fill;
        hatch: Hatch;
    };
}
export interface Box extends Box.Attrs {
}
export declare abstract class Box extends Glyph {
    properties: Box.Props;
    constructor(attrs?: Partial<Box.Attrs>);
    static initClass(): void;
}
