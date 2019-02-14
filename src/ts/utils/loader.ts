export const loader = makeLoader()

export
function makeLoader(): HTMLDivElement {
  let loader = document.createElement('div');
  loader.classList.add('loader');
  loader.style.display = 'none';
  let loader_icon = document.createElement('div');
  loader_icon.classList.add('loader_icon');
  loader.appendChild(loader_icon);
  return loader
}

export 
function showLoader(close_on_click = false){
  loader.style.display = 'flex';
  if(close_on_click){
    loader.onclick = () => {
      loader.style.display = 'none';
    }
  } else {
    loader.onclick = () => {};
  }
  document.body.appendChild(loader);
}

export 
function hideLoader(minload=200){
  setTimeout(()=> {
    document.body.removeChild(loader);
  }, minload);
}