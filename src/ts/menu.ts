import {CommandRegistry} from '@phosphor/commands';
import {DockPanel,  Menu, MenuBar, Widget} from '@phosphor/widgets';
import {showLoader} from './utils/index';
import {PrimaryTab} from './views';
import {COMMANDS} from './define';

export const commands = new CommandRegistry();

export type MenuPages = {
  main: DockPanel,
  home: Widget,
  notebooks: PrimaryTab,
  jobs: PrimaryTab,
  reports: PrimaryTab,
  status: Widget,
};


function buildHome(pages: MenuPages): Menu {
  let menu = new Menu({ commands });
  menu.title.label = 'Home';
  menu.title.mnemonic = 0;
 
  commands.addCommand(COMMANDS.openHome, {
    label: 'Open', mnemonic: 2, iconClass: 'fa fa-home',
    execute: () => {
      pages.main.addWidget(pages.home);
      pages.main.selectWidget(pages.home);
    }
  });
  menu.addItem({ command: COMMANDS.openHome});
  return menu;
}

function buildNotebooks(pages: MenuPages): Menu {
  let menu = new Menu({ commands });
  menu.title.label = 'Notebooks';
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.browseNotebooks, {
    label: 'Browse', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      pages.main.addWidget(pages.notebooks);
      pages.main.selectWidget(pages.notebooks);
    }
  });

  commands.addCommand(COMMANDS.newNotebook, {
    label: 'New', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      pages.main.addWidget(pages.notebooks.control);
      pages.main.selectWidget(pages.notebooks.control);
    }
  });

  menu.addItem({ command: COMMANDS.browseNotebooks});
  menu.addItem({ command: COMMANDS.newNotebook});
  return menu;
}

function buildJobs(pages: MenuPages): Menu {
  let menu = new Menu({ commands });
  menu.title.label = 'Jobs';
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.browseJobs, {
    label: 'Browse', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      pages.main.addWidget(pages.jobs);
      pages.main.selectWidget(pages.jobs);
    }
  });

  commands.addCommand(COMMANDS.newJob, {
    label: 'New', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      pages.main.addWidget(pages.jobs.control);
      pages.main.selectWidget(pages.jobs.control);
    }
  });

  menu.addItem({ command: COMMANDS.browseJobs});
  menu.addItem({ command: COMMANDS.newJob});

  return menu;
}

function buildReports(pages: MenuPages): Menu {
  let menu = new Menu({ commands });
  menu.title.label = 'Reports';
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.browseReports, {
    label: 'Browse', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      pages.main.addWidget(pages.reports);
      pages.main.selectWidget(pages.reports);
    }
  });

  commands.addCommand(COMMANDS.newReport, {
    label: 'New', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      pages.main.addWidget(pages.reports.control);
      pages.main.selectWidget(pages.reports.control);
    }
  });

  menu.addItem({ command: COMMANDS.browseReports});
  menu.addItem({ command: COMMANDS.newReport});

  return menu;
}

function buildStatus(pages: MenuPages): Menu {
  let menu = new Menu({ commands });
  menu.title.label = 'Status';
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.openStatus, {
    label: 'Open', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      pages.main.addWidget(pages.status);
      pages.main.selectWidget(pages.status);
    }
  });

  menu.addItem({ command: COMMANDS.openStatus});

  return menu;
}


function buildAbout(pages: MenuPages): Menu {
  let about = new Menu({ commands });
  about.title.label = 'About';
  about.title.mnemonic = 0;
 
  commands.addCommand(COMMANDS.openLoader, {
    label: 'Open Loader', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      showLoader(true);
    }
  });

  commands.addCommand(COMMANDS.login, {
    label: 'Login', mnemonic: 2, iconClass: 'fa fa-sign-out',
    execute: () => {
      window.location.href = (document as any).loginurl;
    },
    isEnabled: () => {return (document as any).user === '';}
  });

  commands.addCommand(COMMANDS.logout, {
    label: 'Logout', mnemonic: 2, iconClass: 'fa fa-sign-in',
    execute: () => {
      window.location.href = (document as any).logouturl;
    },
    isEnabled: () => {return (document as any).user !== '';}
  });
  about.addItem({ command: COMMANDS.login});  
  about.addItem({ command: COMMANDS.logout});
  about.addItem({ command: COMMANDS.openLoader});
  return about;
}


export
function buildMenus(bar: MenuBar, pages: MenuPages): void {
  bar.addMenu(buildHome(pages));
  bar.addMenu(buildNotebooks(pages));
  bar.addMenu(buildJobs(pages));
  bar.addMenu(buildReports(pages));
  bar.addMenu(buildStatus(pages));
  bar.addMenu(buildAbout(pages));
}
