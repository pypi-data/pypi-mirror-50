import { GestureTool, GestureToolView } from "./gesture_tool";
import * as p from "../../../core/properties";
import { GestureEvent, ScrollEvent } from "../../../core/ui_events";
import { Dimensions } from "../../../core/enums";
export declare class WheelZoomToolView extends GestureToolView {
    model: WheelZoomTool;
    _pinch(ev: GestureEvent): void;
    _scroll(ev: ScrollEvent): void;
}
export declare namespace WheelZoomTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = GestureTool.Props & {
        dimensions: p.Property<Dimensions>;
        maintain_focus: p.Property<boolean>;
        zoom_on_axis: p.Property<boolean>;
        speed: p.Property<number>;
    };
}
export interface WheelZoomTool extends WheelZoomTool.Attrs {
}
export declare class WheelZoomTool extends GestureTool {
    properties: WheelZoomTool.Props;
    constructor(attrs?: Partial<WheelZoomTool.Attrs>);
    static initClass(): void;
    tool_name: string;
    icon: string;
    event_type: "scroll" | "pinch";
    default_order: number;
    readonly tooltip: string;
}
