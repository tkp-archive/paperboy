import {Widget} from "@phosphor/widgets";
import {deleteAllChildren} from "../dom/common";
import {buildHorizontalTable} from "../dom/horizontalTable";

/*** create paginated table from data ***/
export
function createStatusSection(sec: Widget, clazz: string, data: any): void {
  const table = buildHorizontalTable(data);
  deleteAllChildren(sec.node);
  sec.node.appendChild(table);
}
