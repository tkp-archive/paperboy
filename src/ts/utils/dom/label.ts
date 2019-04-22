
/**
 * Helper function to build a generic label element
 * @param text text to put in label
 */
export
function buildLabel(text: string): HTMLLabelElement {
  const label = document.createElement("label");
  label.textContent = text;
  return label;
}
