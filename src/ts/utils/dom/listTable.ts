import {toProperCase} from "../index";
import {buildGeneric} from "./generic";

/**
 * Helper function to build a variant of the Horizontal table.
 *
 * Used in the primary browsers.
 * @param data JSON data to fill in the table
 * @param ondblclick callback function when a row is double-clicked (e.g. display detail view for row)
 */
export
function buildListTable(data: any,
                        // tslint:disable-next-line: no-empty
                        ondblclick = (id: any) => {}): HTMLTableElement {
  const table = document.createElement("table");
  const headerrow = document.createElement("tr");
  table.appendChild(headerrow);
  let first = true;

  // tslint:disable-next-line: prefer-for-of
  for (let i = 0; i < data.length; i++) {
    const dataRow = data[i];
    const row = document.createElement("tr");

    // tslint:disable-next-line: prefer-for-of
    for (let j = 0; j < dataRow.length; j++) {
      const dat = dataRow[j];

      const name = dat.name;
      const label = dat.label;
      const type = dat.type;
      const value = dat.value;

      if (name === "id") {
        row.ondblclick = () => {ondblclick(value); };
        continue;
      }

      if (first) {
        const n = document.createElement("th");
        n.textContent = toProperCase(label);
        headerrow.appendChild(n);
      }
      const v = document.createElement("td");
      v.appendChild(buildGeneric(type, value, name));
      row.appendChild(v);
    }

    table.appendChild(row);
    first = false;
  }
  return table;
}
