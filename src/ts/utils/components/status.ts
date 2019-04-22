import {Widget} from "@phosphor/widgets";
import {deleteAllChildren} from "../dom/common";
import {buildHorizontalTable} from "../dom/horizontalTable";

/**
 * Helper function to create status monitor table
 * @param sec PhosphorWidget of the item we are monitoring status of
 * @param clazz class of the widget
 * @param data JSON data to populate the horizontal table
 */
export
function createStatusSection(sec: Widget, clazz: string, data: any): void {
  const table = buildHorizontalTable(data);
  deleteAllChildren(sec.node);
  sec.node.appendChild(table);
}
