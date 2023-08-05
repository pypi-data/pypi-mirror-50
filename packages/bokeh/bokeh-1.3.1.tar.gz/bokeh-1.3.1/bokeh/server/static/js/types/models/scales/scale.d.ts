import { Transform } from "../transforms";
import { Range } from "../ranges/range";
import { Range1d } from "../ranges/range1d";
import { Arrayable } from "../../core/types";
import * as p from "../../core/properties";
export declare namespace Scale {
    type Attrs = p.AttrsOf<Props>;
    type Props = Transform.Props & {
        source_range: p.Property<Range>;
        target_range: p.Property<Range1d>;
    };
}
export interface Scale extends Scale.Attrs {
}
export declare abstract class Scale extends Transform {
    properties: Scale.Props;
    constructor(attrs?: Partial<Scale.Attrs>);
    static initClass(): void;
    abstract compute(x: number): number;
    abstract v_compute(xs: Arrayable<number>): Arrayable<number>;
    abstract invert(sx: number): number;
    abstract v_invert(sxs: Arrayable<number>): Arrayable<number>;
    r_compute(x0: number, x1: number): [number, number];
    r_invert(sx0: number, sx1: number): [number, number];
}
