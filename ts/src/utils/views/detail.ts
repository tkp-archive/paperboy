import {buildVerticalTable} from '../dom/index';
import {requestFormData, RequestResult} from '../request';
import {createModal} from '../modal';
import {createErrorDialog} from '../errors';

/*** create detail view from python json response to detail ***/
export
function createDetail(sec: HTMLFormElement, title: any, data: any) : Promise<boolean> {
  return new Promise((resolve) => {
    sec.appendChild(
      buildVerticalTable(data, title, sec, (url: string) => {
        let form = new FormData(sec);
        createRequestModal().then((ok: boolean) => {
          if(ok){
            requestFormData(url, form).then((res: RequestResult) => {
              if(res.ok){
                createResponseModal(res.json()).then(() => {
                  resolve(true);
                  return
                });
              } else {
                createErrorDialog(res);
              }
            });
          } else {
            resolve(false);
          }
        });
      }));     
  });
}

/*** create response modal from python json response to config ***/
function createResponseModal(resp: [{[key: string]: string}]): Promise<boolean> {
  return new Promise((resolve) => {
    createModal(resp, true, false).then(resolve);
  });
}

/*** create request modal to ask "are you sure"? ***/
function createRequestModal(): Promise<boolean> {
  return new Promise((resolve) => {
    createModal([{'type': 'label', 'value': 'Are you sure?'}], true, true).then((ok: boolean)=> {
      if(ok){
        resolve(true);  
      } else {
        resolve(false);
      }
    });
  });
}
