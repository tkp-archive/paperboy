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
  // BoxPanel, DockPanel,  SplitPanel, StackedPanel, CommandPalette, ContextMenu, MenuBar, Widget, DockLayout, Menu
  BoxPanel, DockPanel,  SplitPanel, CommandPalette, ContextMenu, MenuBar, Widget, Menu
} from '@phosphor/widgets';

import '../ts/style/index.css';
import "@jpmorganchase/perspective-viewer";
import "@jpmorganchase/perspective-viewer-hypergrid";
import "@jpmorganchase/perspective-viewer-highcharts";

import {
  PSPWidget
} from './perspective-widget';

import {
    TableWidget
} from './table';

import {
  ControlsWidget
} from './controls';


class Header extends Widget {
    static createNode(): HTMLElement {
        let node = document.createElement('div');
        node.classList.add('header');
        let h = document.createElement('img');
        h.src = "data:image/png;base64,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";
        node.appendChild(h);
        return node;
    }

    constructor(){
        super({ node: Header.createNode() });
        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
        this.node.id = 'header';
    }

    // protected onActivateRequest(msg: Message): void {
    //     if (this.isAttached) {
    //         this.inputNode.focus();
    //     }
    // }
}

const commands = new CommandRegistry();

function addCommands(palette:CommandPalette){
  palette.addItem({
    command: 'save-dock-layout',
    category: 'Dock Layout',
    rank: 0
  });

  palette.addItem({
    command: 'controls:open',
    category: 'Dock Layout',
    rank: 0
  });

  palette.addItem({
    command: 'market-data:open',
    category: 'Dock Layout',
    rank: 0
  });

  palette.addItem({
    command: 'fundamentals:open',
    category: 'Dock Layout',
    rank: 0
  });

  palette.addItem({
    command: 'financials:open',
    category: 'Dock Layout',
    rank: 0
  });

  palette.addItem({
    command: 'metrics:open',
    category: 'Dock Layout',
    rank: 0
  });

  palette.addItem({
    command: 'markets:open',
    category: 'Dock Layout',
    rank: 0
  });
}


function main(): void {
  
  /* File Menu */
  let menu = new Menu({ commands });
  menu.title.label = 'File';
  menu.title.mnemonic = 0;

  menu.addItem({ command: 'controls:open' });
  menu.addItem({ type: 'separator'});

  /* Data Menu */
  let menu2 = new Menu({ commands });
  menu2.title.label = 'Data';
  menu2.title.mnemonic = 0;

  menu2.addItem({ command: 'market-data:open'});
  menu2.addItem({ type: 'separator'});
  menu2.addItem({ command: 'fundamentals:open'});
  menu2.addItem({ command: 'financials:open'});
  menu2.addItem({ type: 'separator'});
  menu2.addItem({ command: 'metrics:open'});
  menu2.addItem({ type: 'separator'});
  menu2.addItem({ command: 'markets:open' });

  /* layouts menu */
  let menu3 = new Menu({ commands });
  menu3.title.label = 'Layout';
  menu3.title.mnemonic = 0;

  menu3.addItem({ command: 'save-dock-layout'});
  menu3.addItem({ type: 'separator'});
  menu3.addItem({ command: 'restore-dock-layout', args: {index: 0}});


  /* Title bar */
  let header = new Header();

  /* File bar */
  let bar = new MenuBar();
  bar.addMenu(menu);
  bar.addMenu(menu2);
  bar.addMenu(menu3);
  bar.id = 'menuBar';

  /* context menu */
  let contextMenu = new ContextMenu({ commands });

  document.addEventListener('contextmenu', (event: MouseEvent) => {
    if (contextMenu.open(event)) {
      event.preventDefault();
    }
  });

  contextMenu.addItem({ command: 'controls:open', selector: '.content' });
  contextMenu.addItem({ type: 'separator', selector: '.p-CommandPalette-input' });
  contextMenu.addItem({ command: 'save-dock-layout', selector: '.content' });
  contextMenu.addItem({ command: 'restore-dock-layout', selector: '.content' });

  document.addEventListener('keydown', (event: KeyboardEvent) => {
    commands.processKeydownEvent(event);
  });


  /* perspectives */
  let performance = new PSPWidget('Performance');  // chart
  let quotes = new PSPWidget('Quotes');  // quote
  let dividends = new PSPWidget('Dividends'); //dividends
  let cashflow = new PSPWidget('Cashflow');
  let financials = new PSPWidget('Financials'); // financials
  let earnings = new PSPWidget('Earnings');
  let peers = new PSPWidget('Peers');
  let markets = new PSPWidget('Markets');
  let peercorrelation = new PSPWidget('PeerCorrelation');
  let composition = new PSPWidget('Composition');

  let psps= {'chart':performance,
             'quote':quotes,
             'dividends': dividends,
             'cashflow': cashflow,
             'financials': financials,
             'earnings': earnings,
             'peers': peers,
             'markets':markets,
             'peerCorrelation': peercorrelation,
             'composition': composition}

  let stats = new TableWidget('Stats');
  let news = new TableWidget('News');
  let tables = {'stats': stats,
                'news': news};

  let ctrl = new ControlsWidget('JPM', psps, tables);

  let dock = new DockPanel();
  dock.id = 'dock';


  /* Reference Data Tab */
  let refdata_panel = new SplitPanel();
  refdata_panel.title.label = 'Fundamentals';
  let stats_and_comp_panel = new BoxPanel({ direction: 'top-to-bottom', spacing: 0 });
  stats_and_comp_panel.addWidget(psps['composition']);
  stats_and_comp_panel.addWidget(news);
  refdata_panel.addWidget(stats);
  refdata_panel.addWidget(stats_and_comp_panel);
  refdata_panel.title.closable = true;

  /* Financials Tab */
  let financials_panel = new SplitPanel();
  let earnings_panel = new BoxPanel({ direction: 'top-to-bottom', spacing: 0 });
  financials_panel.title.label = 'Financials';
  earnings_panel.addWidget(psps['financials']);
  earnings_panel.addWidget(psps['earnings']);
  earnings_panel.addWidget(psps['dividends']);
  financials_panel.addWidget(psps['cashflow']);
  financials_panel.addWidget(earnings_panel);
  financials_panel.title.closable = true;

  /* Metrics Tab */
  let metrics_panel = new BoxPanel({ direction: 'top-to-bottom', spacing: 0 });
  metrics_panel.title.label = 'Calculations';
  metrics_panel.addWidget(psps['peerCorrelation']);
  metrics_panel.addWidget(psps['peers']);
  metrics_panel.title.closable = true;

  /* Market Data Tab */
  let market_data_panel = new BoxPanel({ direction: 'top-to-bottom', spacing: 0 });
  market_data_panel.title.label = 'Market Data';
  market_data_panel.addWidget(psps['chart']);
  market_data_panel.addWidget(psps['quote']);
  market_data_panel.title.closable = true;

  /* Markets Info */
  dock.addWidget(market_data_panel);
  dock.addWidget(refdata_panel, {mode: 'tab-after', ref: market_data_panel});
  dock.addWidget(financials_panel, {mode: 'tab-after', ref: refdata_panel});
  dock.addWidget(metrics_panel, {mode: 'tab-after', ref: financials_panel});
  dock.addWidget(psps['markets'], {mode: 'tab-after', ref: metrics_panel});



  /* save/restore layouts */
  let savedLayouts: DockPanel.ILayoutConfig[] = [];

  /* command palette */
  let palette = new CommandPalette({ commands });
  palette.id = 'palette';
  addCommands(palette);

  // /* command registry */
  commands.addCommand('save-dock-layout', {
    label: 'Save Layout',
    caption: 'Save the current dock layout',
    execute: () => {
      savedLayouts.push(dock.saveLayout());
      palette.addItem({
        command: 'restore-dock-layout',
        category: 'Dock Layout',
        args: { index: savedLayouts.length - 1 }
      });
      menu3.addItem({ command: 'restore-dock-layout', args: {index: savedLayouts.length - 1}});
    }
  });

  commands.addCommand('restore-dock-layout', {
    label: args => {
      return `Restore Layout ${args.index as number}`;
    },
    execute: args => {
      dock.restoreLayout(savedLayouts[args.index as number]);
    }
  });

  // commands.addCommand('controls:open', {
  //   label: 'Controls',
  //   mnemonic: 1,
  //   iconClass: 'fa fa-plus',
  //   execute: () => {
  //     dock.restoreLayout(savedLayouts[0]);
  //   }
  // });

  commands.addCommand('market-data:open', {
    label: 'Open Market Data',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      dock.addWidget(market_data_panel);
    }
  });


  commands.addCommand('fundamentals:open', {
    label: 'Open Fundamentals Data',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      dock.addWidget(refdata_panel);
    }
  });

  commands.addCommand('financials:open', {
    label: 'Open Financials Data',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      dock.addWidget(financials_panel);
    }
  });

  commands.addCommand('metrics:open', {
    label: 'Open Calculations Data',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      dock.addWidget(metrics_panel);
    }
  });

  commands.addCommand('markets:open', {
    label: 'Open Markets',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      dock.addWidget(psps['markets']);
    }
  });

  /* hack for custom sizing */
  // var layout = dock.saveLayout();
  // var sizes: number[] = (layout.main as DockLayout.ISplitAreaConfig).sizes;
  // sizes[0] = 0.6;
  // sizes[1] = 0.4;
  // dock.restoreLayout(layout);
  savedLayouts.push(dock.saveLayout());
  // palette.addItem({
  //   command: 'restore-dock-layout',
  //   category: 'Dock Layout',
  //   args: { index: 0}
  // });

  /* main area setup */
  BoxPanel.setStretch(dock, 1);

  let main = new SplitPanel();
  main.id = 'main';
  main.addWidget(ctrl);
  main.addWidget(dock);
  main.setRelativeSizes([.3, .7]);

  window.onresize = () => { main.update(); };

  Widget.attach(header, document.body);
  Widget.attach(bar, document.body);
  Widget.attach(main, document.body);

  setTimeout(()=>{ctrl.start()}, 500);
}


window.onload = main;
