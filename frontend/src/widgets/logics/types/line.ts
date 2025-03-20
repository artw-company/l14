export type LineStyle = {
  stroke: string;
  strokeWidth: number;
  fill: string;
  opacity?: number;
};

export type OutlineStyle = LineStyle & {
  strokeOpacity?: number;
};

export interface LineData {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  style?: LineStyle;
  outlineStyle?: OutlineStyle;
}
