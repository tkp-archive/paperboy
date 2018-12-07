import {buildGeneric, deleteAllChildren} from './dom/index';

const modal = document.createElement('div');
modal.classList.add('modal');

export
function createModal(data: {[key:string]: string}[],
                     ok=true,
                     cancel=true,
                     ok_callback=()=>{},
                     cancel_callback=()=>{}): Promise<void> {
  deleteAllChildren(modal);

  for(let i=0; i<data.length; i++){
    let dat = data[i];
    modal.appendChild(buildGeneric(dat['type'], dat['value']))
  }

  document.body.appendChild(modal);

  return new Promise((resolve) => {
    if(ok){
      let button = buildGeneric('button', 'OK');
      button.onclick = () => {
        ok_callback();
        resolve(hideModal());
      }
      modal.appendChild(button);
      button.focus()
    }
    if(cancel){
      let button = buildGeneric('button', 'Cancel');
      button.onclick = () => {
        cancel_callback();
        resolve(hideModal());
      }
      modal.appendChild(button);
    }
  });
}

export
function hideModal(): Promise<void>{
    return new Promise((resolve) => {
      document.body.removeChild(modal);
      resolve();
    })
}
