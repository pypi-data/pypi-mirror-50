import { Transform } from "./transform";
import { ColumnarDataSource } from "../sources/columnar_data_source";
import * as p from "../../core/properties";
import { Arrayable } from "../../core/types";
export declare namespace Interpolator {
    type Attrs = p.AttrsOf<Props>;
    type Props = Transform.Props & {
        x: p.Property<string | number[]>;
        y: p.Property<string | number[]>;
        data: p.Property<ColumnarDataSource | null>;
        clip: p.Property<boolean>;
    };
}
export interface Interpolator extends Interpolator.Attrs {
}
export declare abstract class Interpolator extends Transform {
    properties: Interpolator.Props;
    constructor(attrs?: Partial<Interpolator.Attrs>);
    static initClass(): void;
    protected _x_sorted: number[];
    protected _y_sorted: number[];
    protected _sorted_dirty: boolean;
    connect_signals(): void;
    v_compute(xs: Arrayable<number>): Arrayable<number>;
    sort(descending?: boolean): void;
}
