import {buildGeneric} from './dom/index';

const modal = document.createElement('div');
modal.classList.add('modal');

export
function createModal(ok=true, cancel=true, ok_callback=()=>{}, cancel_callback=()=>{}){
  document.body.appendChild(modal);
  if(ok){
    let button = buildGeneric('button', 'OK');
    button.onclick = () => {
      ok_callback();
    }
    modal.appendChild(button);
    button.focus()
  }
  if(cancel){
    let button = buildGeneric('button', 'Cancel');
    button.onclick = () => {
      cancel_callback();
    }
    modal.appendChild(button);
  }
  return modal
}

export
function hideModal(){
    document.body.removeChild(modal);
}
