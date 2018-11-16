import {buildVerticalTable, buildGeneric} from '../dom/index';
import {createModal} from '../modal';

/*** create config from python json ***/
export
function createConfigForm(sec: HTMLFormElement | null, clazz: string, data: any, callback=()=>{}) : void {
  if(! sec){
    return;
  }

  sec.appendChild(buildVerticalTable(data));

  // for(let i=0; i<data.length; i++){
  //   let name = data[i]['name'];
  //   let type = data[i]['type'];

  //   if(data[i]['label']){
  //     sec.appendChild(buildLabel(data[i]['label']));
  //   }

  //   switch(type){
  //     case 'label': {
  //       //no more
  //       break;
  //     }
  //     case 'text': {}
  //     case 'file': {}
  //     case 'checkbox': {}
  //     case 'datetime': {
  //       let input = buildInput(type, name, data[i]['placeholder'], data[i]['value'], data[i]['required']);
  //       sec.appendChild(input);
  //       break;
  //     }
  //     case 'textarea': {
  //       let input = buildTextarea(name, data[i]['placeholder'], data[i]['value'], data[i]['required']);
  //       sec.appendChild(input);
  //       break;
  //     }
  //     case 'json': {
  //       let input = buildTextarea(name, data[i]['placeholder'], data[i]['value'], data[i]['required'], true);
  //       sec.appendChild(input);
  //       break;
  //     }
  //     case 'submit': {
  //       let input = buildInput(type, name, data[i]['placeholder'], data[i]['value'], data[i]['required']);
  //       sec.appendChild(input);
  //       sec.onsubmit = () => {
  //         let form = new FormData(sec);
  //         requestFormData(data[i]['url'], form).then((res: RequestResult) => {
  //           createResponseModal(res.json(), callback);
  //         });
  //         return false;
  //       };
  //       break;
  //     }
  //     case 'autocomplete': {
  //       let auto = buildAutocomplete(name, data[i]['url'], data[i]['required']);
  //       sec.appendChild(auto[0]);
  //       sec.appendChild(auto[1]);
  //       break;
  //     }
  //     case 'select': {
  //       let select = buildSelect(name, data[i]['options']);
  //       sec.appendChild(select);
  //       break;
  //     }
  //   }
  // }
}




/*** create response modal from python json response to config ***/
export
function createResponseModal(resp: [{[key: string]: string}], callback= ()=> {}): void {
  let modal = createModal(true, false, callback);
  for(let i=0; i<resp.length; i++){
    let dat = resp[i];
    modal.appendChild(buildGeneric(dat['type'], dat['value']))
  }
}

