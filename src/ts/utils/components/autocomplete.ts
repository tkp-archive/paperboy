import {deleteAllChildren} from "../dom/index";
import {IRequestResult, request} from "../request";

/**
 * Helper function to autocomplete against a server endpoint and
 * fill in a HTMLDataList
 * @param path path to query server with partial entry
 * @param value value representing the partial entry to autocomplete
 * @param autocomplete HTMLDataListEleemnt to fill in with results
 */
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

/**
 * Build an autocomplete searchbox
 * @param name name of dom node
 * @param url url to hit for reqults
 * @param required is an entry required for the autocomplete input?
 */
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
