import { GroupTotals } from "slickgrid";
import * as p from "../../../core/properties";
import { Model } from "../../../model";
export declare namespace RowAggregator {
    type Attrs = p.AttrsOf<Props>;
    type Props = Model.Props & {
        field_: p.Property<string>;
    };
}
export interface RowAggregator extends RowAggregator.Attrs {
    readonly key: string;
}
export declare abstract class RowAggregator extends Model {
    properties: RowAggregator.Props;
    constructor(attrs?: Partial<RowAggregator.Attrs>);
    static initClass(): void;
    abstract init(): void;
    abstract accumulate(item: {
        [key: string]: any;
    }): void;
    abstract storeResult(totals: GroupTotals<number>): void;
}
export declare class AvgAggregator extends RowAggregator {
    readonly key = "avg";
    static initClass(): void;
    init: () => void;
    accumulate: (item: unknown) => void;
    storeResult: (groupTotals: GroupTotals<unknown>) => void;
}
export declare class MinAggregator extends RowAggregator {
    readonly key = "min";
    static initClass(): void;
    init: () => void;
    accumulate: (item: unknown) => void;
    storeResult: (groupTotals: GroupTotals<unknown>) => void;
}
export declare class MaxAggregator extends RowAggregator {
    readonly key = "max";
    static initClass(): void;
    init: () => void;
    accumulate: (item: unknown) => void;
    storeResult: (groupTotals: GroupTotals<unknown>) => void;
}
export declare class SumAggregator extends RowAggregator {
    readonly key = "sum";
    static initClass(): void;
    init: () => void;
    accumulate: (item: unknown) => void;
    storeResult: (groupTotals: GroupTotals<unknown>) => void;
}
