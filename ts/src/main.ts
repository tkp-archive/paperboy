import {
  TabPanel,  SplitPanel, MenuBar, Widget
} from '@phosphor/widgets';

import {Header, Status, Browser, Notebooks, Jobs, Reports} from './views/index';
import {showLoader, hideLoader} from './utils/index';
import {buildMenu} from './menu';
import '../ts/style/index.css';


export
function main(): void {
  showLoader();

  /* Title bar */
  let header = new Header();

  let home = new SplitPanel();
  home.title.label = "Home";

  let overview = new Status();
  let notebooks = new Notebooks(overview);
  let jobs = new Jobs(overview);
  let reports = new Reports(overview);

  home.addWidget(new Browser(notebooks, jobs, reports, overview));

  let main = new TabPanel();
  main.id = 'main';

  main.addWidget(home);
  main.addWidget(notebooks);
  main.addWidget(jobs);
  main.addWidget(reports);
  main.addWidget(overview);

  window.onresize = () => { main.update(); };

  /* File bar */
  let bar = new MenuBar();
  bar.addMenu(buildMenu());
  bar.id = 'menuBar';

  Widget.attach(header, document.body);
  Widget.attach(bar, document.body);
  Widget.attach(main, document.body);

  hideLoader(1000);
}


window.onload = main;
