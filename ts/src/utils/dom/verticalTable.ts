import {toProperCase} from '../index';
import {buildInput} from './input';
import {buildAutocomplete} from '../autocomplete';

export
function buildVerticalTable(data: any, title?: any): HTMLTableElement {
  let table = document.createElement('table');
  for(let i=0; i<data.length; i++){
      let row = document.createElement('tr');
      let td1 = document.createElement('td');
      let td2 = document.createElement('td');

      if(data[i]['name'] === 'name'){
        if (title){
          title.label = data[i]['value'];
        }
      }
      td1.textContent = toProperCase(data[i]['name']);
      row.appendChild(td1);

      let type = data[i]['type'];

      if(type !== 'label'){
        switch(type){
          case 'submit': {
            let input = buildInput(type, name, data[i]['placeholder'], data[i]['value'], data[i]['required']);
            td2.appendChild(input);
            // td.onsubmit = () => {
            //   let form = new FormData(sec);
            //   requestFormData(data[i]['url'], form).then((res: RequestResult) => {
            //     createResponseModal(res.json(), callback);
            //   });
            //   return false;
            // };
            // break;
            break
          }
          case 'autocomplete': {
            let auto = buildAutocomplete(name, data[i]['url'], data[i]['required']);
            td2.appendChild(auto[0]);
            td2.appendChild(auto[1]);
            break;
          }
          default: {
            let conts = buildInput(data[i]['type'], 
                    data[i]['name'],
                    data[i]['placeholder'],
                    data[i]['value'],
                    data[i]['required'],
                    data[i]['readonly'],
                    data[i]['options'],
                    (data[i]['type'] == 'json'));
            td2.appendChild(conts);
          }
        }
        row.appendChild(td2);
      }
      table.appendChild(row);
  }
  return table;
}
