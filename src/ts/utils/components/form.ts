import {buildVerticalTable} from "../dom/index";
import {createModal} from "../modal";
import {IRequestResult, requestFormData} from "../request";

/*** create config from python json ***/
export
function createConfigForm(sec: HTMLFormElement | null,
                          clazz: string,
                          data: any,
                          // tslint:disable-next-line: no-empty
                          callback= () => {}): Promise<boolean> {
return new Promise((resolve) => {
    if (! sec) {
      resolve(false);
      return;
    }

    sec.appendChild(buildVerticalTable(data, "", sec, (url: string) => {
      const form = new FormData(sec);
      requestFormData(url, form).then((res: IRequestResult) => {
        createResponseModal(res.json()).then(() => {
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
    createModal(resp, true, false).then(() => {
      resolve(true);
    });
  });
}
