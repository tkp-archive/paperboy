import {Widget} from '@phosphor/widgets';
import {buildHorizontalTable} from '../dom/horizontalTable';
import {deleteAllChildren} from '../dom/common';

/*** create paginated table from data ***/
export
function createStatusSection(sec: Widget, clazz: string, data: any) : void {
  let table = buildHorizontalTable(data);
  deleteAllChildren(sec.node);
  sec.node.appendChild(table);
}

