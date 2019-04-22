import {DockPanel, MenuBar, Widget} from "@phosphor/widgets";

import "../src/style/index.css";
import {hideLoader, showLoader} from "./utils/index";
import {Browser, buildMenus, Header, Jobs, Notebooks, Reports, Status} from "./views/index";

export
function main(): void {
  showLoader();

  /* Title bar */
  const header = new Header();

  /* main layout */
  // tslint:disable-next-line: no-shadowed-variable
  const main = new DockPanel();
  main.id = "main";

  /* home browser */
  const status = new Status();
  const notebooks = new Notebooks(main, status);
  const jobs = new Jobs(main, status);
  const reports = new Reports(main, status);
  const browser = new Browser(notebooks, jobs, reports, status);
  browser.title.label = "Home";
  browser.title.closable = true;
  main.addWidget(browser);

  /* File bar */
  const bar = new MenuBar();
  bar.id = "menuBar";
  buildMenus(bar, {
    home: browser,
    jobs,
    main,
    notebooks,
    reports,
    status,
  });

  window.onresize = () => { main.update(); };

  Widget.attach(header, document.body);
  Widget.attach(bar, document.body);
  Widget.attach(main, document.body);

  hideLoader(1000);
}

window.onload = main;
