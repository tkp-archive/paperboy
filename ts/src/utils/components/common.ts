import {deleteAllChildren, buildListTable} from '../dom/index';
import {showLoader, hideLoader} from '../loader';
import {PrimaryTab} from '../../views/index';


/*** create paginated table from data ***/
export
function createPrimarySection(widget: PrimaryTab, clazz: string, data: any, paginate=(page: number)=>{}) : void {
  let sec = widget.mine;
  deleteAllChildren(sec.node);
  let page = data['page'];
  let pages = data['pages'];
  // let count = data['count'];
  let total = data['total'];
  let start = (page-1)*25 + 1;
  let end = Math.min((page)*25, total);
  
  let results = data['results'];
  if(results.length > 0) {
    let table = buildListTable(results, (id:any)=>{
      showLoader();
      widget.detailView(id);
      hideLoader();
    })
    // only add table if it has data
    
    sec.node.appendChild(table);
  }
  
  let p1 = document.createElement('p');
  p1.textContent = 'Showing ' + start + ' to ' + end + ' of ' + total;
  
  let p2 = document.createElement('p');
  for(let i = 1; i <= pages; i++){
    let span = document.createElement('span');
    span.textContent = i + ' ';
    if (i === page){
      span.classList.add('page-active');
    } else {
      span.classList.add('page');
    }
    // callback on page click
    span.addEventListener('click', (ev: MouseEvent)=> {
      showLoader();
      paginate(i);
      hideLoader();
    });
    p2.appendChild(span);
  }
  
  sec.node.appendChild(p1);
  sec.node.appendChild(p2);
}