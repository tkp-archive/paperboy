import {DockPanel,  SplitPanel, MenuBar, Widget} from '@phosphor/widgets';

import {Header, Status, Browser, Notebooks, Jobs, Reports} from './views/index';
import {showLoader, hideLoader} from './utils/index';
import {buildMenus} from './menu';
import '../src/style/index.css';


export
function main(): void {
  showLoader();

  /* Title bar */
  let header = new Header();

  /* main layout */
  let main = new DockPanel();
  main.id = 'main';


  /* home browser */
  let home = new SplitPanel();
  home.title.label = "Home";
  home.title.closable = true;


  let status = new Status();
  let notebooks = new Notebooks(main, status);
  let jobs = new Jobs(main, status);
  let reports = new Reports(main, status);

  let browser = new Browser(notebooks, jobs, reports, status);
  home.addWidget(browser);

  main.addWidget(home);
  // main.addWidget(notebooks);
  // main.addWidget(jobs);
  // main.addWidget(reports);
  // main.addWidget(overview);


  /* File bar */
  let bar = new MenuBar();
  bar.id = 'menuBar';
  buildMenus(bar, {
    main,
    home,
    notebooks,
    jobs,
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
