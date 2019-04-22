export const loader = makeLoader();

/**
 * helper function to create global modal with a spinner in it
 * Note: this is designed to be a singleton
 */
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

/**
 * helper function to show global modal with spinner in it
 * @param closeOnClick should we close the modal if the user clicks (for debug)
 */
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

/**
 * Hide the global modal with spinner in it
 * @param minload hide after minload milliseconds
 */
export
function hideLoader(minload= 200) {
  setTimeout(() => {
    document.body.removeChild(loader);
  }, minload);
}
