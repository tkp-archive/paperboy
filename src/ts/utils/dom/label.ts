
/*** build a label ***/
export
function buildLabel(text: string): HTMLLabelElement {
  const label = document.createElement("label");
  label.textContent = text;
  return label;
}
