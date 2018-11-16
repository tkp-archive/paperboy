import {deleteAllChildren, buildVerticalTable} from '../dom/index';


/*** create detail view from python json response to detail ***/
export
function createDetail(data: any, title: any, node: HTMLElement){
    deleteAllChildren(node);
    let table = buildVerticalTable(data, title);
    node.appendChild(table);
}
