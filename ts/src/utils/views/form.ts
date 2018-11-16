import {buildVerticalTable} from '../dom/index';
import {requestFormData, RequestResult} from '../request';
import {createModal} from '../modal';

/*** create config from python json ***/
export
function createConfigForm(sec: HTMLFormElement | null, clazz: string, data: any, callback=()=>{}) : void {
  if(! sec){
    return;
  }

  sec.appendChild(buildVerticalTable(data, '', sec, (url:string)=>{
    let form = new FormData(sec);
    requestFormData(url, form).then((res: RequestResult) => {
      createResponseModal(res.json(), callback);
    });
    return false;
  }));
}




/*** create response modal from python json response to config ***/
export
function createResponseModal(resp: [{[key: string]: string}], callback= ()=> {}): void {
  createModal(resp, true, false, callback);
}

