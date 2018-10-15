/*-----------------------------------------------------------------------------
| Copyright (c) 2014-2017, PhosphorJS Contributors
|
| Distributed under the terms of the BSD 3-Clause License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
import 'es6-promise/auto';  // polyfill Promise on IE

import {
  CommandRegistry
} from '@phosphor/commands';

import {
  TabPanel, BoxPanel,  SplitPanel, MenuBar, Widget, Menu
} from '@phosphor/widgets';

import {Header} from './header';
import {Status} from './status';
import {QuickBrowser} from './quickbrowser';
import {Browser} from './browser';
import {Notebooks} from './notebooks';
import {Jobs} from './jobs';
import {Reports} from './reports';

import '../ts/style/index.css';
import "@jpmorganchase/perspective-viewer";
import "@jpmorganchase/perspective-viewer-hypergrid";
import "@jpmorganchase/perspective-viewer-highcharts";

const commands = new CommandRegistry();

function main(): void {
  /* Home "Menu" */
  let menu = new Menu({ commands });
  menu.title.label = 'About';
  menu.title.mnemonic = 0;

  /* Title bar */
  let header = new Header();

  /* File bar */
  let bar = new MenuBar();
  bar.addMenu(menu);
  bar.id = 'menuBar';

  document.addEventListener('keydown', (event: KeyboardEvent) => {
    commands.processKeydownEvent(event);
  });

  let home = new SplitPanel();
  home.title.label = "Home";

  let overview = new BoxPanel({ direction: 'top-to-bottom', spacing: 0 });
  overview.title.label = "Overview"
  overview.addWidget(new Status());
  overview.addWidget(new QuickBrowser());

  home.addWidget(overview);
  home.addWidget(new Browser());

  home.setRelativeSizes([.3, .7]);

  let main = new TabPanel();
  main.id = 'main';

  main.addWidget(home);
  main.addWidget(new Notebooks());
  main.addWidget(new Jobs());
  main.addWidget(new Reports());

  window.onresize = () => { main.update(); };

  Widget.attach(header, document.body);
  Widget.attach(bar, document.body);
  Widget.attach(main, document.body);
}


window.onload = main;
