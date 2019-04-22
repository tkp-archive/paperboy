import {CommandRegistry} from "@phosphor/commands";
import {DockPanel,  Menu, MenuBar, Widget} from "@phosphor/widgets";
import {COMMAND_ICONS, COMMAND_LABELS, COMMANDS} from "../define";
import {showLoader} from "../utils/index";
import {PrimaryTab} from "./index";

export const commands = new CommandRegistry();

export interface IMenuPages {
  main: DockPanel;
  home: Widget;
  notebooks: PrimaryTab;
  jobs: PrimaryTab;
  reports: PrimaryTab;
  status: Widget;
}

function buildFile(pages: IMenuPages): Menu {
  const menu = new Menu({ commands });
  menu.title.label = "File";
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.openHome, {
    execute: () => {
      pages.main.addWidget(pages.home);
      pages.main.selectWidget(pages.home);
    },
    iconClass: COMMAND_ICONS.openHome,
    label: COMMAND_LABELS.openHome,
    mnemonic: 2,
  });
  menu.addItem({ command: COMMANDS.openHome});

  commands.addCommand(COMMANDS.browseNotebooks, {
    execute: () => {
      pages.main.addWidget(pages.notebooks);
      pages.main.selectWidget(pages.notebooks);
    },
    iconClass: COMMAND_ICONS.browseNotebooks,
    label: COMMAND_LABELS.browseNotebooks,
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.browseJobs, {
    execute: () => {
      pages.main.addWidget(pages.jobs);
      pages.main.selectWidget(pages.jobs);
    },
    iconClass: COMMAND_ICONS.browseJobs,
    label: COMMAND_LABELS.browseJobs,
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.browseReports, {
    execute: () => {
      pages.main.addWidget(pages.reports);
      pages.main.selectWidget(pages.reports);
    },
    iconClass: COMMAND_ICONS.browseReports,
    label: COMMAND_LABELS.browseReports,
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.openStatus, {
    execute: () => {
      pages.main.addWidget(pages.status);
      pages.main.selectWidget(pages.status);
    },
    iconClass: COMMAND_ICONS.openStatus,
    label: COMMAND_LABELS.openStatus,
    mnemonic: 2,
  });

  menu.addItem({ command: COMMANDS.openStatus});
  menu.addItem({ command: COMMANDS.browseNotebooks});
  menu.addItem({ command: COMMANDS.browseJobs});
  menu.addItem({ command: COMMANDS.browseReports});
  return menu;
}

function buildNew(pages: IMenuPages): Menu {
  const menu = new Menu({ commands });
  menu.title.label = "Add";
  menu.title.mnemonic = 0;

  commands.addCommand(COMMANDS.newNotebook, {
    execute: () => {
      pages.main.addWidget(pages.notebooks.control);
      pages.main.selectWidget(pages.notebooks.control);
    },
    iconClass: COMMAND_ICONS.newNotebook,
    label: COMMAND_LABELS.newNotebook,
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.newJob, {
    execute: () => {
      pages.main.addWidget(pages.jobs.control);
      pages.main.selectWidget(pages.jobs.control);
    },
    iconClass: COMMAND_ICONS.newJob,
    label: COMMAND_LABELS.newJob,
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.newReport, {
    execute: () => {
      pages.main.addWidget(pages.reports.control);
      pages.main.selectWidget(pages.reports.control);
    },
    iconClass: COMMAND_ICONS.newReport,
    label: COMMAND_LABELS.newReport,
    mnemonic: 2,
  });

  menu.addItem({ command: COMMANDS.newNotebook});
  menu.addItem({ command: COMMANDS.newJob});
  menu.addItem({ command: COMMANDS.newReport});

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
    iconClass: COMMAND_ICONS.openLoader,
    label: COMMAND_LABELS.openLoader,
    mnemonic: 2,
  });

  commands.addCommand(COMMANDS.login, {
    execute: () => {
      window.location.href = (document as any).loginurl;
    },
    iconClass: COMMAND_ICONS.login,
    isEnabled: () => (document as any).user === "",
    label: COMMAND_LABELS.login,
    mnemonic: 2,

  });

  commands.addCommand(COMMANDS.logout, {
    execute: () => {
      window.location.href = (document as any).logouturl;
    },
    iconClass: COMMAND_ICONS.logout,
    isEnabled: () => (document as any).user !== "",
    label: COMMAND_LABELS.logout,
    mnemonic: 2,
  });
  about.addItem({ command: COMMANDS.login});
  about.addItem({ command: COMMANDS.logout});
  about.addItem({ command: COMMANDS.openLoader});
  return about;
}

export
function buildMenus(bar: MenuBar, pages: IMenuPages): void {
  bar.addMenu(buildFile(pages));
  bar.addMenu(buildNew(pages));
  bar.addMenu(buildAbout(pages));
}
