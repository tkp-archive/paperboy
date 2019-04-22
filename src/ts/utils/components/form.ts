import {buildVerticalTable} from "../dom/index";
import {IRequestResult, requestFormData} from "../request";
import {createModal} from "./modal";

/**
 * Helper function to build a configuration editor into a vertical table
 * @param sec form to put the config in
 * @param clazz unused
 * @param data JSON data to populate the form with
 * @param callback callback on form submission (save/cancel)
 */
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

/**
 * Helper function to create a modal response from submission of the above form
 * @param resp JSON data for response
 */
export
function createResponseModal(resp: [{[key: string]: string}]): Promise<boolean> {
  return new Promise((resolve) => {
    createModal(resp, true, false).then(() => {
      resolve(true);
    });
  });
}
