import {toProperCase} from "../index";

/**
 * Build a generic html table where data is displayed with
 * keys in the top row and items in the rows beneath.
 *
 * Used in the status viewer.
 * @param data JSON data to fill into table
 */
export
function buildHorizontalTable(data: any): HTMLTableElement {
  const table = document.createElement("table");
  const headerrow = document.createElement("tr");
  const name = document.createElement("th");
  name.textContent = "Name";
  headerrow.appendChild(name);
  table.appendChild(headerrow);

  let first = true;
  // tslint:disable-next-line: prefer-for-of
  for (let i = 0; i < data.length; i++) {
    const dat = data[i];
    const row = document.createElement("tr");
    const v = document.createElement("td");
    v.textContent = dat.name;
    row.appendChild(v);

    for (const k of Object.keys(dat.meta)) {
      if (first) {
        // tslint:disable-next-line: no-shadowed-variable
        const name = document.createElement("th");
        name.textContent = toProperCase(k);
        headerrow.appendChild(name);
      }
      // tslint:disable-next-line: no-shadowed-variable
      const v = document.createElement("td");
      v.textContent = dat.meta[k];
      row.appendChild(v);
    }
    table.appendChild(row);
    first = false;
  }
  return table;
}
