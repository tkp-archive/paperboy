import {deleteAllChildren} from "../dom/index";
import {IRequestResult, request} from "../request";

/*** autocomplete key/name pairs from server ***/
export
// tslint:disable-next-line: no-shadowed-variable
function autocomplete(path: string, value: string, autocomplete: HTMLDataListElement) {
    request("get", path).then((res: IRequestResult) => {
        const jsn =  res.json() as any;
        if (jsn) {
            deleteAllChildren(autocomplete);

            for (const val of jsn) {
                const option = document.createElement("option");
                option.value = val.id;
                option.innerText = val.id + " - " + val.name;
                autocomplete.appendChild(option);
            }
        }
    });
}

/*** build an autocomplete ***/
export
function buildAutocomplete(name: string, url: string, required= false): [HTMLInputElement, HTMLDataListElement] {
  const search = document.createElement("input");

  if (required) {
    search.required = true;
  }

  search.setAttribute("list", name + "-datalist");
  search.placeholder = "Search...";
  search.name = name;
  search.autocomplete = "off";

  const datalist = document.createElement("datalist");
  datalist.id = name + "-datalist";

  let last = "";
  search.addEventListener("input", () => {
    deleteAllChildren(datalist);
  });

  search.addEventListener("keyup", () => {
    if (last !== search.value) {
      autocomplete(url + search.value, search.value, datalist);
    }
    last = search.value;
  });
  search.addEventListener("mousedown", () => {
    deleteAllChildren(datalist);
  });

  return [search, datalist];
}
