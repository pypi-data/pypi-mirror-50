import * as p from "../../../core/properties";
import { DOMView } from "../../../core/dom_view";
import { Model } from "../../../model";
import { Item } from "./table_column";
export declare abstract class CellEditorView extends DOMView {
    model: CellEditor;
    defaultValue: any;
    readonly emptyValue: any;
    inputEl: HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;
    protected args: any;
    protected abstract _createInput(): HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;
    constructor(options: any);
    initialize(): void;
    css_classes(): string[];
    render(): void;
    renderEditor(): void;
    disableNavigation(): void;
    destroy(): void;
    focus(): void;
    show(): void;
    hide(): void;
    position(): any;
    getValue(): any;
    setValue(val: any): void;
    serializeValue(): any;
    isValueChanged(): boolean;
    applyValue(item: Item, state: any): void;
    loadValue(item: Item): void;
    validateValue(value: any): any;
    validate(): any;
}
export declare namespace CellEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = Model.Props;
}
export interface CellEditor extends CellEditor.Attrs {
}
export declare abstract class CellEditor extends Model {
    properties: CellEditor.Props;
}
export declare class StringEditorView extends CellEditorView {
    model: StringEditor;
    inputEl: HTMLInputElement;
    readonly emptyValue: string;
    protected _createInput(): HTMLInputElement;
    renderEditor(): void;
    loadValue(item: Item): void;
}
export declare namespace StringEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props & {
        completions: p.Property<string[]>;
    };
}
export interface StringEditor extends StringEditor.Attrs {
}
export declare class StringEditor extends CellEditor {
    properties: StringEditor.Props;
    static initClass(): void;
}
export declare class TextEditorView extends CellEditorView {
    model: TextEditor;
    inputEl: HTMLTextAreaElement;
    protected _createInput(): HTMLTextAreaElement;
}
export declare namespace TextEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props;
}
export interface TextEditor extends TextEditor.Attrs {
}
export declare class TextEditor extends CellEditor {
    properties: TextEditor.Props;
    static initClass(): void;
}
export declare class SelectEditorView extends CellEditorView {
    model: SelectEditor;
    inputEl: HTMLSelectElement;
    protected _createInput(): HTMLSelectElement;
    renderEditor(): void;
}
export declare namespace SelectEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props & {
        options: p.Property<string[]>;
    };
}
export interface SelectEditor extends SelectEditor.Attrs {
}
export declare class SelectEditor extends CellEditor {
    properties: SelectEditor.Props;
    static initClass(): void;
}
export declare class PercentEditorView extends CellEditorView {
    model: PercentEditor;
    inputEl: HTMLInputElement;
    protected _createInput(): HTMLInputElement;
}
export declare namespace PercentEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props;
}
export interface PercentEditor extends PercentEditor.Attrs {
}
export declare class PercentEditor extends CellEditor {
    properties: PercentEditor.Props;
    static initClass(): void;
}
export declare class CheckboxEditorView extends CellEditorView {
    model: CheckboxEditor;
    inputEl: HTMLInputElement;
    protected _createInput(): HTMLInputElement;
    renderEditor(): void;
    loadValue(item: Item): void;
    serializeValue(): any;
}
export declare namespace CheckboxEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props;
}
export interface CheckboxEditor extends CheckboxEditor.Attrs {
}
export declare class CheckboxEditor extends CellEditor {
    properties: CheckboxEditor.Props;
    static initClass(): void;
}
export declare class IntEditorView extends CellEditorView {
    model: IntEditor;
    inputEl: HTMLInputElement;
    protected _createInput(): HTMLInputElement;
    renderEditor(): void;
    remove(): void;
    serializeValue(): any;
    loadValue(item: Item): void;
    validateValue(value: any): any;
}
export declare namespace IntEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props & {
        step: p.Property<number>;
    };
}
export interface IntEditor extends IntEditor.Attrs {
}
export declare class IntEditor extends CellEditor {
    properties: IntEditor.Props;
    static initClass(): void;
}
export declare class NumberEditorView extends CellEditorView {
    model: NumberEditor;
    inputEl: HTMLInputElement;
    protected _createInput(): HTMLInputElement;
    renderEditor(): void;
    remove(): void;
    serializeValue(): any;
    loadValue(item: Item): void;
    validateValue(value: any): any;
}
export declare namespace NumberEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props & {
        step: p.Property<number>;
    };
}
export interface NumberEditor extends NumberEditor.Attrs {
}
export declare class NumberEditor extends CellEditor {
    properties: NumberEditor.Props;
    static initClass(): void;
}
export declare class TimeEditorView extends CellEditorView {
    model: TimeEditor;
    inputEl: HTMLInputElement;
    protected _createInput(): HTMLInputElement;
}
export declare namespace TimeEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props;
}
export interface TimeEditor extends TimeEditor.Attrs {
}
export declare class TimeEditor extends CellEditor {
    properties: TimeEditor.Props;
    static initClass(): void;
}
export declare class DateEditorView extends CellEditorView {
    model: DateEditor;
    inputEl: HTMLInputElement;
    protected _createInput(): HTMLInputElement;
    readonly emptyValue: Date;
    renderEditor(): void;
    destroy(): void;
    show(): void;
    hide(): void;
    position(): any;
    getValue(): any;
    setValue(_val: any): void;
}
export declare namespace DateEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = CellEditor.Props;
}
export interface DateEditor extends DateEditor.Attrs {
}
export declare class DateEditor extends CellEditor {
    properties: DateEditor.Props;
    static initClass(): void;
}
