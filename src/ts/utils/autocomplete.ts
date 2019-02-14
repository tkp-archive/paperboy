import {request, RequestResult} from './request';
import {deleteAllChildren} from './dom/index';

/*** autocomplete key/name pairs from server ***/
export
function autocomplete(path: string, value: string, autocomplete: HTMLDataListElement){
    request('get', path).then((res: RequestResult) => {
        var jsn = <any>res.json();
        if (jsn) {
            deleteAllChildren(autocomplete);

            for(let val of jsn){
                let option = document.createElement('option');
                option.value = val['id'];
                option.innerText = val['id'] + ' - ' + val['name'];
                autocomplete.appendChild(option);
            }
        }
    });
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
    deleteAllChildren(datalist);
  });

  search.addEventListener('keyup', () => {
    if(last != search.value){
      autocomplete(url + search.value, search.value, datalist);
    }
    last = search.value;
  });
  search.addEventListener('mousedown', () => {
    deleteAllChildren(datalist);
  });

  return [search, datalist];
}
