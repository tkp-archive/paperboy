import {
    Widget
} from '@phosphor/widgets';

import {request, requestFormData, RequestResult} from './request';
import {PrimaryTab} from './common';

export
function baseurl(){
  return (document as any).baseurl || '/';
}

export
function apiurl(){
  return (document as any).apiurl || '/api/v1/';
}

/*** Title Case formatter ***/
export
function toProperCase(str: string) {
  return str.replace(/\w\S*/g, function(txt: string){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

/*** autocomplete key/name pairs from server ***/
export
function autocomplete(path: string, value: string, autocomplete: HTMLDataListElement){
    request('get', path).then((res: RequestResult) => {
        var jsn = <any>res.json();
        if (jsn) {
            DomUtils.delete_all_children(autocomplete);

            for(let val of jsn){
                let option = document.createElement('option');
                option.value = val['id'];
                option.innerText = val['id'] + ' - ' + val['name'];
                autocomplete.appendChild(option);
            }
        }
    });
}


/*** A collection of dom builders ***/
export
namespace DomUtils {
  /*** require select ***/
  let default_none = document.createElement('option');
  default_none.selected = false;
  default_none.disabled = true;
  default_none.hidden = false;
  default_none.style.display = 'none';
  default_none.value = '';


  /*** delete all children of element helper ***/
  export
  function delete_all_children(element: HTMLElement): void{
    while(element.lastChild){
      element.removeChild(element.lastChild);
    }
  }

  /*** build a label ***/
  export 
  function buildLabel(text: string): HTMLLabelElement {
    let label = document.createElement('label');
    label.textContent = text;
    return label;
  }

  /*** build a textarea ***/
  export 
  function buildTextarea(name?: string,
                         placeholder?: string,
                         value?: string,
                         required = false,
                         json = false
                      ){
    let area = document.createElement('textarea');
    if(name){
      area.name = name;
    }
    if(placeholder){
      area.placeholder = placeholder;
    }
    if(value){
      if(json){
        area.value = JSON.stringify(JSON.parse(value), undefined, 4);
        area.classList.add('json');
      } else {
        area.value = value;
      }
    }
    area.required = required;
    area.style.marginBottom = '15px';
    return area;
  }


  /*** build a select ***/
  export
  function buildSelect(name: string,
                       list: string[],
                       def?: string,
                       required = false,
                       readonly = false): HTMLSelectElement {
    let select = document.createElement('select');
    select.name = name;
    if(required){
      select.required = required;
    }
    if(readonly){
      select.disabled = true;
    }

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

  /*** build an autocomplete ***/
  export
  function buildAutocomplete(name: string, url: string, required=false): [HTMLInputElement, HTMLDataListElement] {
    let search = document.createElement('input');

    if(required){
      search.required = true;
    }

    search.setAttribute('list', name + '-datalist');
    search.placeholder = 'Search...';
    search.name = name;
    search.autocomplete = 'off';

    let datalist = document.createElement('datalist');
    datalist.id = name + '-datalist';

    let last = '';
    search.addEventListener('input', ()=>{
      delete_all_children(datalist);
    });

    search.addEventListener('keyup', () => {
      if(last != search.value){
        autocomplete(url + search.value, search.value, datalist);
      }
      last = search.value;
    });
    search.addEventListener('mousedown', () => {
      delete_all_children(datalist);
    });

    return [search, datalist];
  }


  /*** build an input ***/
  /***
    allowed:
      - text
      - file
      - checkbox
      - date picker
      - submit button
      - select
      - textarea
      - autocomplete
   ***/
  export
  function buildInput(type?: string,
                      name?: string,
                      placeholder?: string,
                      value?: string,
                      required = false,
                      readonly = false,
                      options = [],
                      json = false
                      ): HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement {
    if (!type ){
      type = 'text';
    }

    let input = document.createElement('input');
    if(required){
      input.required = true;
    }
    if(readonly){
      input.readOnly = true;
      input.disabled = true;
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
        let d = new Date();
        input.value = d.toISOString().slice(0,16);
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
      case 'select': {
        return buildSelect(name || '', options, value, required, readonly);
      }
      case 'textarea': {}
      case 'json': {
        return buildTextarea(name || '', placeholder, value, required, json);
      }
    }
    return input;
  }

  /*** build a generic element ***/
  /***
    allowed:
    - br
    - span
    - p
    - button
    - h1
    - h2
    - h3
    - h4
    - h5
    - h6
    - label
   ***/
  export
  function buildGeneric(type: string, content?: string): HTMLElement {
    switch(type) {
      case 'br': {}
      case 'span': {}
      case 'p': {}
      case 'button': {}
      case 'h1': {}
      case 'h2': {}
      case 'h3': {}
      case 'h4': {}
      case 'h5': {}
      case 'h6': {
        let d = document.createElement(type);
        d.textContent = content || '';
        return d;
      }
      case 'label': {
        return buildLabel(content || '');
      }
      default: {
        return document.createElement('div');
      }
    }
  }

  export
  function buildHorizontalTable(data: any, ondblclick = (dat:any)=> {}): HTMLTableElement {
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
      row.ondblclick = () => {ondblclick(dat);};
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

  export
  function buildVerticalTable(data: any, title: any): HTMLTableElement {
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

        let conts = DomUtils.buildInput(data[i]['type'], 
                data[i]['name'],
                data[i]['placeholder'],
                data[i]['value'],
                data[i]['required'],
                data[i]['readonly'],
                data[i]['options'],
                (data[i]['type'] == 'json'));

        td2.appendChild(conts);

        row.appendChild(td1);
        row.appendChild(td2);
        table.appendChild(row);
    }
    return table;
  }

  /*** create paginated table from data ***/
  export
  function createStatusSection(sec: Widget, clazz: string, data: any) : void {
    let table = buildHorizontalTable(data);
    delete_all_children(sec.node);
    sec.node.appendChild(table);
  }

  /*** create paginated table from data ***/
  export
  function createPrimarySection(widget: PrimaryTab, clazz: string, data: any, paginate=(page: number)=>{}) : void {
    let sec = widget.mine;
    delete_all_children(sec.node);
    let page = data['page'];
    let pages = data['pages'];
    let count = data['count'];
    let total = data['total'];
    
    let results = data['results'];
    if(results.length > 0) {
      let table = buildHorizontalTable(results, (dat:any)=>{
        widget.detailView(dat['id']);
      })
      // only add table if it has data
      
      sec.node.appendChild(table);
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
      // callback on page click
      span.addEventListener('click', (ev: MouseEvent)=> {paginate(i);});
      p2.appendChild(span);
    }
    
    sec.node.appendChild(p1);
    sec.node.appendChild(p2);
  }

  /*** create response modal from python json response to config ***/
  export
  function createResponseModal(resp: [{[key: string]: string}], callback= ()=> {}): void {
    let modal = document.createElement('div');
    modal.classList.add('modal');

    for(let i=0; i<resp.length; i++){
      let dat = resp[i];
      modal.appendChild(buildGeneric(dat['type'], dat['value']))
    }

    let button = buildGeneric('button', 'OK');
    button.onclick = () => {
      document.body.removeChild(modal);
      callback();
    }
    modal.appendChild(button);
    document.body.appendChild(modal);
    button.focus();
  }


  /*** create detail view from python json response to detail ***/
  export
  function createDetail(data: any, title: any, node: HTMLElement){
    delete_all_children(node);
    let table = buildVerticalTable(data, title);
    node.appendChild(table);
  }


  /*** create config from python json ***/
  /***
    allowed:
      - label
      - text
      - textarea
      - file
      - checkbox
      - date picker
      - submit button
  ***/
  export
  function createConfigForm(sec: HTMLFormElement | null, clazz: string, data: any, callback=()=>{}) : void {
    if(! sec){
      return;
    }
    for(let i=0; i<data.length; i++){
      let name = data[i]['name'];
      let type = data[i]['type'];

      if(data[i]['label']){
        sec.appendChild(buildLabel(data[i]['label']));
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
          let input = buildInput(type, name, data[i]['placeholder'], data[i]['value'], data[i]['required']);
          sec.appendChild(input);
          break;
        }
        case 'textarea': {
          let input = buildTextarea(name, data[i]['placeholder'], data[i]['value'], data[i]['required']);
          sec.appendChild(input);
          break;
        }
        case 'json': {
          let input = buildTextarea(name, data[i]['placeholder'], data[i]['value'], data[i]['required'], true);
          sec.appendChild(input);
          break;
        }
        case 'submit': {
          let input = buildInput(type, name, data[i]['placeholder'], data[i]['value'], data[i]['required']);
          sec.appendChild(input);
          sec.onsubmit = () => {
            let form = new FormData(sec);
            requestFormData(data[i]['url'], form).then((res: RequestResult) => {
              createResponseModal(res.json(), callback);
            });
            return false;
          };
          break;
        }
        case 'autocomplete': {
          let auto = buildAutocomplete(name, data[i]['url'], data[i]['required']);
          sec.appendChild(auto[0]);
          sec.appendChild(auto[1]);
          break;
        }
        case 'select': {
          let select = buildSelect(name, data[i]['options']);
          sec.appendChild(select);
          break;
        }
      }
    }
  }
}