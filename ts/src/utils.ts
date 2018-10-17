import {
    Widget
} from '@phosphor/widgets';

import {request, requestFormData, RequestResult} from './request';


export
function toProperCase(str: string) {
  return str.replace(/\w\S*/g, function(txt: string){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

export
function autocomplete(path: string, value: string, autocomplete: HTMLDataListElement){
    request('get', path).then((res: RequestResult) => {
        var jsn = <any>res.json();
        if (jsn) {
            DomUtils.delete_all_children(autocomplete);

            for(let val of jsn){
                let option = document.createElement('option');
                option.value = val['key'];
                option.innerText = val['key'] + ' - ' + val['name'];
                autocomplete.appendChild(option);
            }
        }
    });
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
  function buildInput(type?: string,
                      name?: string,
                      placeholder?: string,
                      value?: string,
                      required = false,
                      ){
    if (! type ){
      type = 'text';
    }

    let input = document.createElement('input');
    if(required){
      input.required = true;
    }

    switch(type) {
      case 'text': {
        input.type = type;
        if(placeholder){
          input.placeholder = placeholder;
        }
        if(value){
          input.value = value;
        }
        if(name){
          input.name = name;
        }
        break;
      }
      case 'file': {
        input.type = type;
        if(name){
          input.name = name;
        }
        input.multiple = false;
        break;
      }
      case 'checkbox': {
        input.type = type;
        if(name){
          input.name = name;
        }
        if(value){
          input.checked = true;
        }
        break;
      }
      case 'datetime': {
        input.type = 'datetime-local';
        if(name){
          input.name = name;
        }
        break;        
      }
      case 'submit': {
        input.type = type;
        if(value){
          input.value = value;
        }
        if(name){
          input.name = name;
        }
        break;
      }
    }
    return input;
  }

  export 
  function buildTextarea(text: string): HTMLTextAreaElement {
    let area = document.createElement('textarea');
    area.placeholder = text;
    area.style.marginBottom = '15px';
    return area;
  }


  export
  function buildSelect(name: string, list: string[], def?: string): HTMLSelectElement {
    let select = document.createElement('select');
    select.name = name;

    select.appendChild(default_none);
    for(let i=0; i<list.length; i++) {
      let x = list[i];
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
  function buildAutocomplete(url: string, name: string, required=false): [HTMLInputElement, HTMLDataListElement] {
    let search = document.createElement('input');

    if(required){
      search.required = true;
    }

    search.setAttribute('list', name + '-datalist');
    search.placeholder = 'Search...';
    search.name = name;

    let datalist = document.createElement('datalist');
    datalist.id = name + '-datalist';

    search.addEventListener('keyup', (e: KeyboardEvent) => {
      delete_all_children(datalist);
      autocomplete(url + search.value, search.value, datalist);
    });
    return [search, datalist];
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

  export
  function createConfig(sec: HTMLFormElement | null, clazz: string, data: any) : void {
    if(! sec){
      return;
    }
    for(let k of Object.keys(data)){
      let type = data[k]['type'];

      if(data[k]['label']){
        sec.appendChild(buildLabel(data[k]['label']));
      }

      switch(type){
        case 'label': {
          //no more
          break;
        }
        case 'text': {}
        case 'file': {}
        case 'checkbox': {}
        case 'datetime': {
          let input = buildInput(type, k, data[k]['placeholder'], data[k]['value'], data[k]['required']);
          sec.appendChild(input);
          break;
        }
        case 'submit': {
          let input = buildInput(type, k, data[k]['placeholder'], data[k]['value'], data[k]['required']);
          sec.appendChild(input);
          sec.onsubmit = () => {
            let form = new FormData(sec);
            requestFormData(data[k]['url'], form).then((res: RequestResult) => {
              alert(res);
            });
            return false;
          };

          // sec.action = data[k]['url'];
          // sec.method = 'post';
          break;
        }
        case 'autocomplete': {
          let auto = buildAutocomplete(data[k]['url'], k, data[k]['required']);
          sec.appendChild(auto[0]);
          sec.appendChild(auto[1]);
          break;
        }
        case 'select': {
          let select = buildSelect(k, data[k]['options']);
          sec.appendChild(select);
          break;
        }
      }
    }
  }
}