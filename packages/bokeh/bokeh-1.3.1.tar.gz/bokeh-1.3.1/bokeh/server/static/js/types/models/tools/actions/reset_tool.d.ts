import { ActionTool, ActionToolView } from "./action_tool";
import * as p from "../../../core/properties";
export declare class ResetToolView extends ActionToolView {
    model: ResetTool;
    doit(): void;
}
export declare namespace ResetTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = ActionTool.Props;
}
export interface ResetTool extends ResetTool.Attrs {
}
export declare class ResetTool extends ActionTool {
    properties: ResetTool.Props;
    constructor(attrs?: Partial<ResetTool.Attrs>);
    static initClass(): void;
    tool_name: string;
    icon: string;
}
