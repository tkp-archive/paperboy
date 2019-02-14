import {toProperCase} from '../index';
import {buildGeneric} from './generic';


export
function buildListTable(data: any, ondblclick = (id:any)=> {}): HTMLTableElement {
  let table = document.createElement('table');
  let headerrow = document.createElement('tr');
  table.appendChild(headerrow);
  let first = true;

  for(let i=0; i<data.length; i++){
    let data_row = data[i];
    let row = document.createElement('tr');

    for(let j=0; j<data_row.length; j++){
      let dat = data_row[j];

      let name = dat['name'];
      let label = dat['label'];
      let type = dat['type'];
      let value = dat['value'];

      if(name === 'id'){
        row.ondblclick = () => {ondblclick(value);};
        continue;
      }

      if(first){
        let n = document.createElement('th');
        n.textContent = toProperCase(label);
        headerrow.appendChild(n);
      }
      let v = document.createElement('td');
      v.appendChild(buildGeneric(type, value, name));
      row.appendChild(v);
    }

    table.appendChild(row);
    first = false;
  }
  return table;    
}