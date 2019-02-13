import {CommandRegistry} from '@phosphor/commands';
import {Menu} from '@phosphor/widgets';
import {showLoader} from './utils/index';


export const commands = new CommandRegistry();

export
function buildMenu(): Menu {
  /* Home "Menu" */
  let menu = new Menu({ commands });
  menu.title.label = 'About';
  menu.title.mnemonic = 0;
 
  commands.addCommand('open-loader', {
    label: 'Open Loader', mnemonic: 2, iconClass: 'fa fa-plus',
    execute: () => {
      showLoader(true);
    }
  });

  commands.addCommand('login', {
    label: 'Login', mnemonic: 2, iconClass: 'fa fa-sign-out',
    execute: () => {
      window.location.href = (document as any).loginurl;
    },
    isEnabled: () => {return (document as any).user === '';}
  });

  commands.addCommand('logout', {
    label: 'Logout', mnemonic: 2, iconClass: 'fa fa-sign-in',
    execute: () => {
      window.location.href = (document as any).logouturl;
    },
    isEnabled: () => {return (document as any).user !== '';}
  });
  menu.addItem({ command: 'login'});
  menu.addItem({ command: 'logout'});
  menu.addItem({ command: 'open-loader'});
  return menu;
}
