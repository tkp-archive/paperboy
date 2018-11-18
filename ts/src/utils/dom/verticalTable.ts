import {toProperCase} from '../index';
import {buildInput} from './input';
import {buildAutocomplete} from '../autocomplete';

export
function buildVerticalTable(data: any, title?: any, form?: HTMLFormElement, form_callback=(url?:string)=>{}): HTMLTableElement {
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
      if(!data[i]['hidden']){
        row.appendChild(td1);
      }

      let type = data[i]['type'];

      if(type !== 'label'){
        switch(type){
          case 'submit': {
            let input = buildInput(type, name, data[i]['placeholder'], data[i]['value'], data[i]['required'],data[i]['readonly'], data[i]['hidden']);
            td2.appendChild(input);
            if(form && form_callback){
              let url = data[i]['url'];
              // doesnt work right
              // input.setAttribute('formaction', url);

              // workaround
              // these better not be reordered!!
              input.onclick = ()=>{
                form.action = url;
              }
              form.onsubmit = () => {
                return form_callback(form.action);
              };
            }
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
                    data[i]['hidden'],
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
