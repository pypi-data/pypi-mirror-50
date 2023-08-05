import * as p from "../../../core/properties";
import { Color } from "../../../core/types";
import { FontStyle, TextAlign, RoundingFunction } from "../../../core/enums";
import { Model } from "../../../model";
export declare namespace CellFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = Model.Props;
}
export interface CellFormatter extends CellFormatter.Attrs {
}
export declare abstract class CellFormatter extends Model {
    properties: CellFormatter.Props;
    constructor(attrs?: Partial<CellFormatter.Attrs>);
    doFormat(_row: any, _cell: any, value: any, _columnDef: any, _dataContext: any): string;
}
export declare namespace StringFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellFormatter.Props & {
        font_style: p.Property<FontStyle>;
        text_align: p.Property<TextAlign>;
        text_color: p.Property<Color>;
    };
}
export interface StringFormatter extends StringFormatter.Attrs {
}
export declare class StringFormatter extends CellFormatter {
    properties: StringFormatter.Props;
    constructor(attrs?: Partial<StringFormatter.Attrs>);
    static initClass(): void;
    doFormat(_row: any, _cell: any, value: any, _columnDef: any, _dataContext: any): string;
}
export declare namespace NumberFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = StringFormatter.Props & {
        format: p.Property<string>;
        language: p.Property<string>;
        rounding: p.Property<RoundingFunction>;
    };
}
export interface NumberFormatter extends NumberFormatter.Attrs {
}
export declare class NumberFormatter extends StringFormatter {
    properties: NumberFormatter.Props;
    constructor(attrs?: Partial<NumberFormatter.Attrs>);
    static initClass(): void;
    doFormat(row: any, cell: any, value: any, columnDef: any, dataContext: any): string;
}
export declare namespace BooleanFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellFormatter.Props & {
        icon: p.Property<string>;
    };
}
export interface BooleanFormatter extends BooleanFormatter.Attrs {
}
export declare class BooleanFormatter extends CellFormatter {
    properties: BooleanFormatter.Props;
    constructor(attrs?: Partial<BooleanFormatter.Attrs>);
    static initClass(): void;
    doFormat(_row: any, _cell: any, value: any, _columnDef: any, _dataContext: any): string;
}
export declare namespace DateFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellFormatter.Props & {
        format: p.Property<string>;
    };
}
export interface DateFormatter extends DateFormatter.Attrs {
}
export declare class DateFormatter extends CellFormatter {
    properties: DateFormatter.Props;
    constructor(attrs?: Partial<DateFormatter.Attrs>);
    static initClass(): void;
    getFormat(): string | undefined;
    doFormat(row: any, cell: any, value: any, columnDef: any, dataContext: any): string;
}
export declare namespace HTMLTemplateFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellFormatter.Props & {
        template: p.Property<string>;
    };
}
export interface HTMLTemplateFormatter extends HTMLTemplateFormatter.Attrs {
}
export declare class HTMLTemplateFormatter extends CellFormatter {
    properties: HTMLTemplateFormatter.Props;
    constructor(attrs?: Partial<HTMLTemplateFormatter.Attrs>);
    static initClass(): void;
    doFormat(_row: any, _cell: any, value: any, _columnDef: any, dataContext: any): string;
}
