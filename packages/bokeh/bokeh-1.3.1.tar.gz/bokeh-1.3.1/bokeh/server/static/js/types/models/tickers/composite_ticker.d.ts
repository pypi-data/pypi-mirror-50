import { TickSpec } from "./ticker";
import { ContinuousTicker } from "./continuous_ticker";
import * as p from "../../core/properties";
export declare namespace CompositeTicker {
    type Attrs = p.AttrsOf<Props>;
    type Props = ContinuousTicker.Props & {
        tickers: p.Property<ContinuousTicker[]>;
    };
}
export interface CompositeTicker extends CompositeTicker.Attrs {
}
export declare class CompositeTicker extends ContinuousTicker {
    properties: CompositeTicker.Props;
    constructor(attrs?: Partial<CompositeTicker.Attrs>);
    static initClass(): void;
    readonly min_intervals: number[];
    readonly max_intervals: number[];
    readonly min_interval: number;
    readonly max_interval: number;
    get_best_ticker(data_low: number, data_high: number, desired_n_ticks: number): ContinuousTicker;
    get_interval(data_low: number, data_high: number, desired_n_ticks: number): number;
    get_ticks_no_defaults(data_low: number, data_high: number, cross_loc: any, desired_n_ticks: number): TickSpec<number>;
}
