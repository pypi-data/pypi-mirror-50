import { AbstractSlider, AbstractSliderView } from "./abstract_slider";
import * as p from "../../core/properties";
export declare class DateSliderView extends AbstractSliderView {
    model: DateSlider;
}
export declare namespace DateSlider {
    type Attrs = p.AttrsOf<Props>;
    type Props = AbstractSlider.Props;
}
export interface DateSlider extends DateSlider.Attrs {
}
export declare class DateSlider extends AbstractSlider {
    properties: DateSlider.Props;
    constructor(attrs?: Partial<DateSlider.Attrs>);
    static initClass(): void;
    behaviour: "tap";
    connected: boolean[];
    protected _formatter(value: number, format: string): string;
}
