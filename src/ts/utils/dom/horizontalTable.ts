import {toProperCase} from '../index';

export
function buildHorizontalTable(data: any): HTMLTableElement {
  let table = document.createElement('table');
  let headerrow = document.createElement('tr');
  let name = document.createElement('th');
  name.textContent = 'Name';
  headerrow.appendChild(name);
  table.appendChild(headerrow);

  let first = true;
  for(let i=0; i<data.length; i++){
    let dat = data[i];
    let row = document.createElement('tr');
    let v = document.createElement('td');
    v.textContent = dat['name'];
    row.appendChild(v);

    for(let k of Object.keys(dat['meta'])){
      if(first){
        let name = document.createElement('th');
        name.textContent = toProperCase(k);
        headerrow.appendChild(name);
      }
      let v = document.createElement('td');
      v.textContent = dat['meta'][k];
      row.appendChild(v);
    }
    table.appendChild(row);
    first = false;
  }
  return table;    
}
