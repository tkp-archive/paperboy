import {DockPanel, MenuBar, Widget} from "@phosphor/widgets";

import "../src/style/index.css";
import {hideLoader, showLoader} from "./utils/index";
import {Browser, buildMenus, Header, Jobs, Notebooks, Reports, Outputs, Status} from "./views/index";

export
function main(): void {
  /* show spinner to cover up page load */
  showLoader();

  /* Title bar with logo and light/dark mode buttons */
  const header = new Header();

  /* main layout */
  // tslint:disable-next-line: no-shadowed-variable
  const main = new DockPanel();
  main.id = "main";

  /* Create Status page  */
  const status = new Status();
  /* Create Notebooks page */
  const notebooks = new Notebooks(main, status);
  /* Create Jobs page */
  const jobs = new Jobs(main, status);
  /* Create Reports page */
  const reports = new Reports(main, status);
  /* Create Outputs page */
  const outputs = new Outputs(main, status);

  /* Create Search browser page */
  const browser = new Browser(notebooks, jobs, reports, outputs, status);

  browser.title.label = "Home";
  browser.title.closable = true;
  /* Only show search by default, the rest are hidden in menus */
  main.addWidget(browser);

  /* File bar */
  const bar = new MenuBar();
  bar.id = "menuBar";

  /* Build menu items out of main management tools */
  buildMenus(bar, {
    home: browser,
    jobs,
    main,
    notebooks,
    reports,
    outputs,
    status,
  });

  /* hook in window resize to top phosphor widget */
  window.onresize = () => { main.update(); };

  /* Header */
  Widget.attach(header, document.body);
  /* Menu bar */
  Widget.attach(bar, document.body);
  /* Main dock panel with searchbar opened */
  Widget.attach(main, document.body);

  hideLoader(1000);
}

window.onload = main;
