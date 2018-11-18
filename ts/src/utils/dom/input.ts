import {buildSelect} from './select';
import {buildTextarea} from './textarea';

/*** build an input ***/
export
function buildInput(type?: string,
                    name?: string,
                    placeholder?: string,
                    value?: string,
                    required = false,
                    readonly = false,
                    hidden = false,
                    options = [],
                    json = false
                    ): HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement {
  if (!type ){
    type = 'text';
  }

  if(hidden){
    type = 'hidden';
  }

  let input = document.createElement('input');
  if(required){
    input.required = true;
  }
  if(readonly){
    input.readOnly = true;
    input.disabled = true;
  }

  switch(type) {
    case 'hidden': {}
    case 'text': {
      input.type = type;
      if(placeholder){
        input.placeholder = placeholder;
      }
      if(value){
        input.value = value;
      }
      if(name){
        input.name = name;
      }
      break;
    }
    case 'file': {
      input.type = type;
      if(name){
        input.name = name;
      }
      input.multiple = false;
      break;
    }
    case 'checkbox': {
      input.type = type;
      if(name){
        input.name = name;
      }
      if(value){
        input.checked = true;
      }
      break;
    }
    case 'datetime': {
      input.type = 'datetime-local';
      if(name){
        input.name = name;
      }
      let d = new Date();
      input.value = d.toISOString().slice(0,16);
      break;        
    }
    case 'submit': {
      input.type = type;
      if(value){
        input.value = value;
      }
      if(name){
        input.name = name;
      }
      break;
    }
    case 'select': {
      return buildSelect(name || '', options, value, required, readonly);
    }
    case 'textarea': {}
    case 'json': {
      return buildTextarea(name || '', placeholder, value, required, json);
    }
  }
  return input;
}