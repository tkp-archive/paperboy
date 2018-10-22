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
  TabPanel,  SplitPanel, MenuBar, Widget, Menu
} from '@phosphor/widgets';

import {Header} from './header';
import {Status} from './status';
import {Browser} from './browser';
import {Notebooks} from './notebooks';
import {Jobs} from './jobs';
import {Reports} from './reports';

import '../ts/style/index.css';

const commands = new CommandRegistry();

function makeLoader(): HTMLDivElement {
  let loader = document.createElement('div');
  loader.classList.add('loader');
  loader.style.display = 'none';
  let loader_icon = document.createElement('div');
  loader_icon.classList.add('loader_icon');
  loader.appendChild(loader_icon);
  loader.onclick = () => {
    loader.style.display = 'none';
    document.body.removeChild(loader);
  }
  return loader
}


function main(): void {
  /* Home "Menu" */
  let menu = new Menu({ commands });
  menu.title.label = 'About';
  menu.title.mnemonic = 0;
 
  let loader = makeLoader();
  commands.addCommand('open-loader', {
    label: 'Open Loader',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      loader.style.display = 'flex';
      document.body.appendChild(loader);
    }
  });

  commands.addCommand('login', {
    label: 'Login',
    mnemonic: 2,
    iconClass: 'fa fa-sign-out',
    execute: () => {
      window.location.href = (document as any).loginurl;
    },
    isEnabled: () => {return (document as any).user === '';}
  });

  commands.addCommand('logout', {
    label: 'Logout',
    mnemonic: 2,
    iconClass: 'fa fa-sign-in',
    execute: () => {
      window.location.href = (document as any).logouturl;
    },
    isEnabled: () => {return (document as any).user !== '';}
  });
  menu.addItem({ command: 'login'});
  menu.addItem({ command: 'logout'});
  menu.addItem({ command: 'open-loader'});


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

  let overview = new Status();

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
