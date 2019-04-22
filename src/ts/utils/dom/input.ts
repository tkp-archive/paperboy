import {buildSelect} from "./select";
import {buildTextarea} from "./textarea";

/**
 * Helper function to build a generic input type
 * @param type type of input, in <text, file, select, submit, etc..>
 * @param name name of field for form submission
 * @param placeholder text placeholder for field
 * @param value initial/const value for field
 * @param required is field required in form?
 * @param readonly is field readonly in form?
 * @param hidden is field hidden in form?
 * @param options select input has a fixed set of choices
 * @param json textarea can be unstructured or json
 */
export
function buildInput(type?: string,
                    name?: string,
                    placeholder?: string,
                    value?: string,
                    required = false,
                    readonly = false,
                    hidden = false,
                    options = [],
                    json = false,
                    ): HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement {
  if (!type ) {
    type = "text";
  }

  if (hidden) {
    type = "hidden";
  }

  const input = document.createElement("input");
  if (required) {
    input.required = true;
  }
  if (readonly) {
    input.readOnly = true;
    input.style.filter = "opacity(.5)";
  }

  switch (type) {
    // tslint:disable-next-line: no-empty
    case "hidden": {}
    case "text": {
      input.type = type;
      if (placeholder) {
        input.placeholder = placeholder;
      }
      if (value) {
        input.value = value;
      }
      if (name) {
        input.name = name;
      }
      break;
    }
    case "checkbox": {
      input.type = type;
      if (name) {
        input.name = name;
      }
      if (value) {
        input.checked = true;
      }
      break;
    }
    case "datetime": {
      input.type = "datetime-local";
      if (name) {
        input.name = name;
      }
      const d = new Date();
      input.value = d.toISOString().slice(0, 16);
      break;
    }
    case "submit": {
      input.type = type;
      if (value) {
        input.value = value;
      }
      if (name) {
        input.name = name;
      }
      break;
    }
    case "select": {
      return buildSelect(name || "", options, value, required, readonly);
    }
    // tslint:disable-next-line: no-empty
    case "textarea": {}
    case "json": {
      if (value) {
        return buildTextarea(name || "", placeholder, value, required, json);
      } else {
        type = "file";
      }
    }
    case "file": {
      input.type = type;
      if (name) {
        input.name = name;
      }
      input.multiple = false;
      break;
    }
  }
  return input;
}
