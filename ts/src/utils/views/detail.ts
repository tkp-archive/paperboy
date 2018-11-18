import {buildVerticalTable} from '../dom/index';
import {requestFormData, RequestResult} from '../request';
import {createModal} from '../modal';


/*** create detail view from python json response to detail ***/
export
function createDetail(sec: HTMLFormElement | null, title: any, data: any, callback=()=>{}) : void {
  if(! sec){
    return;
  }

  sec.appendChild(buildVerticalTable(data, title, sec, (url:string)=>{
    let form = new FormData(sec);
    requestFormData(url, form).then((res: RequestResult) => {
      createResponseModal(res.json(), callback);
    });
    return false;
  }));
}


/*** create response modal from python json response to config ***/
function createResponseModal(resp: [{[key: string]: string}], callback= ()=> {}): void {
  createModal(resp, true, false, callback);
}

