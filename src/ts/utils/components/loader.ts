export const loader = makeLoader();

export
function makeLoader(): HTMLDivElement {
  // tslint:disable-next-line: no-shadowed-variable
  const loader = document.createElement("div");
  loader.classList.add("loader");
  loader.style.display = "none";
  const loaderIcon = document.createElement("div");
  loaderIcon.classList.add("loader_icon");
  loader.appendChild(loaderIcon);
  return loader;
}

export
function showLoader(closeOnClick = false) {
  loader.style.display = "flex";
  if (closeOnClick) {
    loader.onclick = () => {
      loader.style.display = "none";
    };
  } else {
    // tslint:disable-next-line: no-empty
    loader.onclick = () => {};
  }
  document.body.appendChild(loader);
}

export
function hideLoader(minload= 200) {
  setTimeout(() => {
    document.body.removeChild(loader);
  }, minload);
}
