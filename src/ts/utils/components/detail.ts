import {buildVerticalTable} from "../dom/index";
import {IRequestResult, requestFormData} from "../request";
import {createErrorDialog} from "./errors";
import {createModal} from "./modal";

/**
 * Helper function to create a detail view of an entry
 * @param sec Phosphor widget in which to populate the results
 * @param title title to give to table
 * @param data JSON data representing the details
 */
export
function createDetail(sec: HTMLFormElement, title: any, data: any): Promise<boolean> {
  return new Promise((resolve) => {
    sec.appendChild(
      buildVerticalTable(data, title, sec, (url: string) => {
        const form = new FormData(sec);
        createRequestModal().then((ok: boolean) => {
          if (ok) {
            requestFormData(url, form).then((res: IRequestResult) => {
              if (res.ok) {
                createResponseModal(res.json()).then(() => {
                  resolve(true);
                  return;
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

/**
 * Helper function to create a global modal representing a response from the server
 * (e.g. for successful form submission, error, etc)
 * @param resp JSON response from server
 */
function createResponseModal(resp: [{[key: string]: string}]): Promise<boolean> {
  return new Promise((resolve) => {
    createModal(resp, true, false).then(resolve);
  });
}

/**
 * Helper function to create a form confirmation modal prior to form submission
 * (e.g. "Are you sure you want to save?")
 */
function createRequestModal(): Promise<boolean> {
  return new Promise((resolve) => {
    createModal([{type: "label", value: "Are you sure?"}], true, true).then((ok: boolean) => {
      if (ok) {
        resolve(true);
      } else {
        resolve(false);
      }
    });
  });
}
