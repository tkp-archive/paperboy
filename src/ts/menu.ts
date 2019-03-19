import {CommandRegistry} from "@phosphor/commands";
import {DockPanel,  Menu, MenuBar, Widget} from "@phosphor/widgets";
import {COMMANDS} from "./define";
import {showLoader} from "./utils/index";
import {PrimaryTab} from "./views";

export const commands = new CommandRegistry();

export interface IMenuPages {
  main: DockPanel;
  home: Widget;
  notebooks: PrimaryTab;
  jobs: PrimaryTab;
  reports: PrimaryTab;
  status: Widget;
}

function buildHome(pages: IMenuPages): Menu {
  const menu = new Menu({ commands });
  menu.title.label = "Home";
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.openHome, {
    execute: () => {
      pages.main.addWidget(pages.home);
      pages.main.selectWidget(pages.home);
    },
    iconClass: "fa fa-home",
    label: "Open",
    mnemonic: 2,
  });
  menu.addItem({ command: COMMANDS.openHome});
  return menu;
}

function buildNotebooks(pages: IMenuPages): Menu {
  const menu = new Menu({ commands });
  menu.title.label = "Notebooks";
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.browseNotebooks, {
    execute: () => {
      pages.main.addWidget(pages.notebooks);
      pages.main.selectWidget(pages.notebooks);
    },
    iconClass: "fa fa-plus",
    label: "Browse",
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.newNotebook, {
    execute: () => {
      pages.main.addWidget(pages.notebooks.control);
      pages.main.selectWidget(pages.notebooks.control);
    },
    iconClass: "fa fa-plus",
    label: "New",
    mnemonic: 2,
  });

  menu.addItem({ command: COMMANDS.browseNotebooks});
  menu.addItem({ command: COMMANDS.newNotebook});
  return menu;
}

function buildJobs(pages: IMenuPages): Menu {
  const menu = new Menu({ commands });
  menu.title.label = "Jobs";
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.browseJobs, {
    execute: () => {
      pages.main.addWidget(pages.jobs);
      pages.main.selectWidget(pages.jobs);
    },
    iconClass: "fa fa-plus",
    label: "Browse",
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.newJob, {
    execute: () => {
      pages.main.addWidget(pages.jobs.control);
      pages.main.selectWidget(pages.jobs.control);
    },
    iconClass: "fa fa-plus",
    label: "New",
    mnemonic: 2,
  });

  menu.addItem({ command: COMMANDS.browseJobs});
  menu.addItem({ command: COMMANDS.newJob});

  return menu;
}

function buildReports(pages: IMenuPages): Menu {
  const menu = new Menu({ commands });
  menu.title.label = "Reports";
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.browseReports, {
    execute: () => {
      pages.main.addWidget(pages.reports);
      pages.main.selectWidget(pages.reports);
    },
    iconClass: "fa fa-plus",
    label: "Browse",
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.newReport, {
    execute: () => {
      pages.main.addWidget(pages.reports.control);
      pages.main.selectWidget(pages.reports.control);
    },
    iconClass: "fa fa-plus",
    label: "New",
    mnemonic: 2,
  });

  menu.addItem({ command: COMMANDS.browseReports});
  menu.addItem({ command: COMMANDS.newReport});

  return menu;
}

function buildStatus(pages: IMenuPages): Menu {
  const menu = new Menu({ commands });
  menu.title.label = "Status";
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.openStatus, {
    execute: () => {
      pages.main.addWidget(pages.status);
      pages.main.selectWidget(pages.status);
    },
    iconClass: "fa fa-plus",
    label: "Open",
    mnemonic: 2,
  });

  menu.addItem({ command: COMMANDS.openStatus});

  return menu;
}

function buildAbout(pages: IMenuPages): Menu {
  const about = new Menu({ commands });
  about.title.label = "About";
  about.title.mnemonic = 0;

  commands.addCommand(COMMANDS.openLoader, {
    execute: () => {
      showLoader(true);
    },
    iconClass: "fa fa-plus",
    label: "Open Loader",
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.login, {
    execute: () => {
      window.location.href = (document as any).loginurl;
    },
    iconClass: "fa fa-sign-out",
    isEnabled: () => (document as any).user === "",
    label: "Login",
    mnemonic: 2,

  });

  commands.addCommand(COMMANDS.logout, {
    execute: () => {
      window.location.href = (document as any).logouturl;
    },
    iconClass: "fa fa-sign-in",
    isEnabled: () => (document as any).user !== "",
    label: "Logout",
    mnemonic: 2,
  });
  about.addItem({ command: COMMANDS.login});
  about.addItem({ command: COMMANDS.logout});
  about.addItem({ command: COMMANDS.openLoader});
  return about;
}

export
function buildMenus(bar: MenuBar, pages: IMenuPages): void {
  bar.addMenu(buildHome(pages));
  bar.addMenu(buildNotebooks(pages));
  bar.addMenu(buildJobs(pages));
  bar.addMenu(buildReports(pages));
  bar.addMenu(buildStatus(pages));
  bar.addMenu(buildAbout(pages));
}
