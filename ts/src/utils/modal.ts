import {buildGeneric, deleteAllChildren} from './dom/index';

const modal = document.createElement('div');
modal.classList.add('modal');

export
function createModal(data: {[key:string]: string}[],
                     ok=true,
                     cancel=true,
                     ok_callback=()=>{},
                     cancel_callback=()=>{}){
  deleteAllChildren(modal);

  for(let i=0; i<data.length; i++){
    let dat = data[i];
    modal.appendChild(buildGeneric(dat['type'], dat['value']))
  }

  document.body.appendChild(modal);
  if(ok){
    let button = buildGeneric('button', 'OK');
    button.onclick = () => {
      ok_callback();
      hideModal();
    }
    modal.appendChild(button);
    button.focus()
  }
  if(cancel){
    let button = buildGeneric('button', 'Cancel');
    button.onclick = () => {
      cancel_callback();
      hideModal();
    }
    modal.appendChild(button);
  }
  return modal
}

export
function hideModal(){
    document.body.removeChild(modal);
}
