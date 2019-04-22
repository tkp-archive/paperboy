import {buildGeneric, deleteAllChildren} from "../dom/index";

/**
 * Only do this once to make sure its a singleton
 */
const modal = document.createElement("div");
modal.classList.add("modal");

/**
 * Create the modal by clearing the previous modal and repopulate
 * @param data JSON data to put into the modal
 * @param ok show ok button?
 * @param cancel show cancel button?
 */
export
function createModal(data: Array<{[key: string]: string}>,
                     ok= true,
                     cancel= true): Promise<boolean> {
  deleteAllChildren(modal);

  // tslint:disable-next-line: prefer-for-of
  for (let i = 0; i < data.length; i++) {
    const dat = data[i];
    modal.appendChild(buildGeneric(dat.type, dat.value));
  }

  document.body.appendChild(modal);

  return new Promise((resolve) => {
    if (ok) {
      const button = buildGeneric("button", "OK");
      button.onclick = () => {
        hideModal().then(() => {resolve(true); });
      };
      modal.appendChild(button);
      button.focus();
    }
    if (cancel) {
      const button = buildGeneric("button", "Cancel");
      button.onclick = () => {
        hideModal().then(() => {resolve(false); });
      };
      modal.appendChild(button);
    }
  });
}

/**
 * helper function to hide the global modal
 */
export
function hideModal(): Promise<void> {
    return new Promise((resolve) => {
      document.body.removeChild(modal);
      resolve();
    });
}
