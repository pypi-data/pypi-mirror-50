import { TickFormatter } from "./tick_formatter";
import * as p from "../../core/properties";
export declare namespace BasicTickFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = TickFormatter.Props & {
        precision: p.Property<number | "auto">;
        use_scientific: p.Property<boolean>;
        power_limit_high: p.Property<number>;
        power_limit_low: p.Property<number>;
    };
}
export interface BasicTickFormatter extends BasicTickFormatter.Attrs {
}
export declare class BasicTickFormatter extends TickFormatter {
    properties: BasicTickFormatter.Props;
    constructor(attrs?: Partial<BasicTickFormatter.Attrs>);
    static initClass(): void;
    protected last_precision: number;
    readonly scientific_limit_low: number;
    readonly scientific_limit_high: number;
    doFormat(ticks: number[], _opts: {
        loc: number;
    }): string[];
}
