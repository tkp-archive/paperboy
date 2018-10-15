import {
    Widget
} from '@phosphor/widgets';

export
function toProperCase(str: string) {
  return str.replace(/\w\S*/g, function(txt: string){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}


export
namespace DomUtils {
  let default_none = document.createElement('option');
  default_none.selected = false;
  default_none.disabled = true;
  default_none.hidden = false;
  default_none.style.display = 'none';
  default_none.value = '';

  export 
  function buildLabel(text: string): HTMLLabelElement {
    let label = document.createElement('label');
    label.textContent = text;
    return label;
  }

  export 
  function buildTextarea(text: string): HTMLTextAreaElement {
    let area = document.createElement('textarea');
    area.placeholder = text;
    area.style.marginBottom = '15px';
    return area;
  }


  export
  function buildSelect(list: string[], def?: string): HTMLSelectElement {
    let select = document.createElement('select');
    select.appendChild(default_none);
    for(let x of list) {
      let option = document.createElement('option');
      option.value = x
      option.textContent = x;
      select.appendChild(option);

      if (def && x === def){
        option.selected = true;
      }
    }
    select.style.marginBottom = '15px';
    select.style.minHeight = '25px';
    return select;
  }

  export
  function createSubsection(sec: Widget, clazz: string, data: any) : void {
    let page = data['page'];
    let pages = data['pages'];
    let count = data['count'];
    let total = data['total'];
    
    let notebooks = data[clazz];
    
    let table = document.createElement('table');
    
    let headerrow = document.createElement('tr');
    let name = document.createElement('th');
    name.textContent = 'Name';

    headerrow.appendChild(name);
    table.appendChild(headerrow);

    let first = true;
    for(let nb of notebooks){
      let row = document.createElement('tr');

      let v = document.createElement('td');
      v.textContent = nb['name'];
      row.appendChild(v);

      for(let k of Object.keys(nb['meta'])){
        if(first){
          let name = document.createElement('th');
          name.textContent = toProperCase(k);
          headerrow.appendChild(name);
        }
        let v = document.createElement('td');
        v.textContent = nb['meta'][k];
        row.appendChild(v);
      }
      table.appendChild(row);
      first = false;
    }
    
    let p1 = document.createElement('p');
    p1.textContent = 'Showing ' + count + ' of ' + total;
    
    let p2 = document.createElement('p');
    for(let i = 1; i <= pages; i++){
      let span = document.createElement('span');
      span.textContent = i + ' ';
      if (i === page){
        span.classList.add('page-active');
      } else {
        span.classList.add('page');
      }
      p2.appendChild(span);
    }
    
    sec.node.appendChild(table);
    sec.node.appendChild(p1);
    sec.node.appendChild(p2);
  }

  export
  function delete_all_children(element: HTMLElement): void{
    while(element.lastChild){
      element.removeChild(element.lastChild);
    }
  }
}