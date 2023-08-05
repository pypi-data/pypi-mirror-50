import { TextAnnotation, TextAnnotationView } from "./text_annotation";
import { FontStyle, VerticalAlign, TextAlign, TextBaseline } from "../../core/enums";
import { Size } from "../../core/layout";
import * as mixins from "../../core/property_mixins";
import * as p from "../../core/properties";
export declare class TitleView extends TextAnnotationView {
    model: Title;
    visuals: Title.Visuals;
    initialize(): void;
    protected _get_location(): [number, number];
    render(): void;
    protected _get_size(): Size;
}
export declare namespace Title {
    type Attrs = p.AttrsOf<Props>;
    type Props = TextAnnotation.Props & {
        text: p.Property<string>;
        text_font: p.Property<string>;
        text_font_size: p.FontSizeSpec;
        text_font_style: p.Property<FontStyle>;
        text_color: p.ColorSpec;
        text_alpha: p.NumberSpec;
        vertical_align: p.Property<VerticalAlign>;
        align: p.Property<TextAlign>;
        offset: p.Property<number>;
        text_align: p.Property<TextAlign>;
        text_baseline: p.Property<TextBaseline>;
    } & mixins.BorderLine & mixins.BackgroundFill;
    type Visuals = TextAnnotation.Visuals;
}
export interface Title extends Title.Attrs {
}
export declare class Title extends TextAnnotation {
    properties: Title.Props;
    constructor(attrs?: Partial<Title.Attrs>);
    static initClass(): void;
}
