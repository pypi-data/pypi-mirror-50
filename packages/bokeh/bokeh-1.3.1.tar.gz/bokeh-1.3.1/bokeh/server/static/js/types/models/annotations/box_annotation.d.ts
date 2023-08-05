import { Annotation, AnnotationView } from "./annotation";
import { Signal0 } from "../../core/signaling";
import { LineScalar, FillScalar } from "../../core/property_mixins";
import { Line, Fill } from "../../core/visuals";
import { SpatialUnits, RenderMode } from "../../core/enums";
import * as p from "../../core/properties";
import { BBox } from "../../core/util/bbox";
export declare const EDGE_TOLERANCE = 2.5;
export declare class BoxAnnotationView extends AnnotationView {
    model: BoxAnnotation;
    visuals: BoxAnnotation.Visuals;
    private sleft;
    private sright;
    private sbottom;
    private stop;
    initialize(): void;
    connect_signals(): void;
    render(): void;
    protected _css_box(sleft: number, sright: number, sbottom: number, stop: number): void;
    protected _canvas_box(sleft: number, sright: number, sbottom: number, stop: number): void;
    interactive_bbox(): BBox;
    interactive_hit(sx: number, sy: number): boolean;
    cursor(sx: number, sy: number): string | null;
}
export declare namespace BoxAnnotation {
    type Attrs = p.AttrsOf<Props>;
    type Props = Annotation.Props & LineScalar & FillScalar & {
        render_mode: p.Property<RenderMode>;
        x_range_name: p.Property<string>;
        y_range_name: p.Property<string>;
        top: p.Property<number | null>;
        top_units: p.Property<SpatialUnits>;
        bottom: p.Property<number | null>;
        bottom_units: p.Property<SpatialUnits>;
        left: p.Property<number | null>;
        left_units: p.Property<SpatialUnits>;
        right: p.Property<number | null>;
        right_units: p.Property<SpatialUnits>;
        screen: p.Property<boolean>;
        ew_cursor: p.Property<string | null>;
        ns_cursor: p.Property<string | null>;
        in_cursor: p.Property<string | null>;
    };
    type Visuals = Annotation.Visuals & {
        line: Line;
        fill: Fill;
    };
}
export interface BoxAnnotation extends BoxAnnotation.Attrs {
}
export declare class BoxAnnotation extends Annotation {
    properties: BoxAnnotation.Props;
    constructor(attrs?: Partial<BoxAnnotation.Attrs>);
    static initClass(): void;
    data_update: Signal0<this>;
    initialize(): void;
    update({ left, right, top, bottom }: {
        left: number | null;
        right: number | null;
        top: number | null;
        bottom: number | null;
    }): void;
}
