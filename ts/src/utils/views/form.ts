import {buildVerticalTable} from '../dom/index';
import {requestFormData, RequestResult} from '../request';
import {createModal} from '../modal';

/*** create config from python json ***/
export
function createConfigForm(sec: HTMLFormElement | null, clazz: string, data: any, callback=()=>{}) : Promise<boolean>{
  return new Promise((resolve) => {
    if(! sec){
      resolve(false);
      return;
    }

    sec.appendChild(buildVerticalTable(data, '', sec, (url:string)=>{
      let form = new FormData(sec);
      requestFormData(url, form).then((res: RequestResult) => {
        createResponseModal(res.json()).then(()=>{
          resolve(true);
        });
      });
    }));
  });
}




/*** create response modal from python json response to config ***/
export
function createResponseModal(resp: [{[key: string]: string}]): Promise<boolean> {
  return new Promise((resolve) => {
    createModal(resp, true, false).then(()=> {
      resolve(true);
    });
  });
}

