import { Markup, MarkupView } from "./markup";
import * as p from "../../core/properties";
export declare class PreTextView extends MarkupView {
    model: PreText;
    render(): void;
}
export declare namespace PreText {
    type Attrs = p.AttrsOf<Props>;
    type Props = Markup.Props;
}
export interface PreText extends PreText.Attrs {
}
export declare class PreText extends Markup {
    properties: PreText.Props;
    constructor(attrs?: Partial<PreText.Attrs>);
    static initClass(): void;
}
