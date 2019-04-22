import {buildAutocomplete} from "../components/index";
import {toProperCase} from "../index";
import {buildInput} from "./input";

export
function buildVerticalTable(data: any,
                            title?: any,
                            form?: HTMLFormElement,
                            // tslint:disable-next-line: no-empty
                            formCallback= (url?: string) => {}): HTMLTableElement {
  const table = document.createElement("table");
  // tslint:disable-next-line: prefer-for-of
  for (let i = 0; i < data.length; i++) {
      const row = document.createElement("tr");
      const td1 = document.createElement("td");
      const td2 = document.createElement("td");

      if (data[i].name === "name") {
        if (title) {
          title.label = data[i].value;
        }
      }
      td1.textContent = toProperCase(data[i].name);
      if (!data[i].hidden) {
        row.appendChild(td1);
      }

      const type = data[i].type;
      const hidden = data[i].hidden;
      const name = data[i].name;

      if (hidden) {
        row.style.display = "none";
      }

      if (type !== "label") {
        switch (type) {
          case "submit": {
            const input = buildInput(type,
                                     name,
                                     data[i].placeholder,
                                     data[i].value,
                                     data[i].required,
                                     data[i].readonly,
                                     data[i].hidden);
            td2.appendChild(input);
            if (form && formCallback) {
              const url = data[i].url;
              // doesnt work right
              // input.setAttribute('formaction', url);

              // workaround
              // these better not be reordered!!
              input.onclick = () => {
                form.action = url;
              };
              form.onsubmit = (e: Event) => {
                e.preventDefault();
                e.stopPropagation();
                formCallback(form.action);
                return false;
              };
            }
            break;
          }
          case "autocomplete": {
            const auto = buildAutocomplete(name, data[i].url, data[i].required);
            td2.appendChild(auto[0]);
            td2.appendChild(auto[1]);
            break;
          }
          default: {
            const conts = buildInput(type,
                    name,
                    data[i].placeholder,
                    data[i].value,
                    data[i].required,
                    data[i].readonly,
                    data[i].hidden,
                    data[i].options,
                    (data[i].type === "json"));
            td2.appendChild(conts);
          }
        }
        row.appendChild(td2);
      }
      table.appendChild(row);
  }
  return table;
}
