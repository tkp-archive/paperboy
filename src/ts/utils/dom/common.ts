
/**
 * Helper to delete all children of a dom node
 * @param element node to delete all children
 */
export
function deleteAllChildren(element: HTMLElement): void {
  while (element.lastChild) {
    element.removeChild(element.lastChild);
  }
}
