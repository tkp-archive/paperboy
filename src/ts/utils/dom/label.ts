
/*** build a label ***/
export 
function buildLabel(text: string): HTMLLabelElement {
  let label = document.createElement('label');
  label.textContent = text;
  return label;
}
