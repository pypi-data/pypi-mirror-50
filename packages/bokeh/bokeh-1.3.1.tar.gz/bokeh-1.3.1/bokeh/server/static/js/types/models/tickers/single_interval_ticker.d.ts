import { ContinuousTicker } from "./continuous_ticker";
import * as p from "../../core/properties";
export declare namespace SingleIntervalTicker {
    type Attrs = p.AttrsOf<Props>;
    type Props = ContinuousTicker.Props & {
        interval: p.Property<number>;
    };
}
export interface SingleIntervalTicker extends SingleIntervalTicker.Attrs {
}
export declare class SingleIntervalTicker extends ContinuousTicker {
    properties: SingleIntervalTicker.Props;
    constructor(attrs?: Partial<SingleIntervalTicker.Attrs>);
    static initClass(): void;
    get_interval(_data_low: number, _data_high: number, _n_desired_ticks: number): number;
    readonly min_interval: number;
    readonly max_interval: number;
}
