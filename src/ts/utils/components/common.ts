import {PrimaryTab} from "../../views/index";
import {buildListTable, deleteAllChildren} from "../dom/index";
import {hideLoader, showLoader} from "../loader";

/*** create paginated table from data ***/
export
function createPrimarySection(widget: PrimaryTab,
                              clazz: string,
                              data: any,
                              // tslint:disable-next-line: no-shadowed-variable no-empty
                              paginate= (page: number) => {}): void {
  const sec = widget.mine;
  deleteAllChildren(sec.node);
  const page = data.page;
  const pages = data.pages;
  // let count = data['count'];
  const total = data.total;
  const start = (page - 1) * 25 + 1;
  const end = Math.min((page) * 25, total);

  const results = data.results;
  if (results.length > 0) {
    const table = buildListTable(results, (id: any) => {
      showLoader();
      widget.detailView(id);
      hideLoader();
    });
    // only add table if it has data

    sec.node.appendChild(table);
  }

  const p1 = document.createElement("p");
  p1.textContent = "Showing " + start + " to " + end + " of " + total;

  const p2 = document.createElement("p");
  for (let i = 1; i <= pages; i++) {
    const span = document.createElement("span");
    span.textContent = i + " ";
    if (i === page) {
      span.classList.add("page-active");
    } else {
      span.classList.add("page");
    }
    // callback on page click
    span.addEventListener("click", (ev: MouseEvent) => {
      showLoader();
      paginate(i);
      hideLoader();
    });
    p2.appendChild(span);
  }

  sec.node.appendChild(p1);
  sec.node.appendChild(p2);
}
