
/*** build a textarea ***/
export
function buildTextarea(name?: string,
                       placeholder?: string,
                       value?: string,
                       required = false,
                       json = false,
                    ) {
  const area = document.createElement("textarea");
  if (name) {
    area.name = name;
  }
  if (placeholder) {
    area.placeholder = placeholder;
  }
  if (value) {
    if (json) {
      area.value = JSON.stringify(JSON.parse(value), undefined, 4);
      area.classList.add("json");
    } else {
      area.value = value;
    }
  }
  area.required = required;
  area.style.marginBottom = "15px";
  return area;
}
