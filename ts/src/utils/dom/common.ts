

/*** delete all children of element helper ***/
export
function deleteAllChildren(element: HTMLElement): void{
  while(element.lastChild){
    element.removeChild(element.lastChild);
  }
}