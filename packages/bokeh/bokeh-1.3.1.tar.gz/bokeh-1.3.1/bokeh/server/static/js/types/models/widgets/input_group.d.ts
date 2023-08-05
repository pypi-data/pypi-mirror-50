import { Control, ControlView } from "./control";
import * as p from "../../core/properties";
export declare abstract class InputGroupView extends ControlView {
    model: InputGroup;
    connect_signals(): void;
}
export declare namespace InputGroup {
    type Attrs = p.AttrsOf<Props>;
    type Props = Control.Props;
}
export interface InputGroup extends InputGroup.Attrs {
}
export declare abstract class InputGroup extends Control {
    properties: InputGroup.Props & {
        active: p.Property<unknown>;
    };
    constructor(attrs?: Partial<InputGroup.Attrs>);
}
