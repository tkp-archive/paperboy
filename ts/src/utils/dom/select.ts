/*** require select ***/
let default_none = document.createElement('option');
default_none.selected = false;
default_none.disabled = true;
default_none.hidden = false;
default_none.style.display = 'none';
default_none.value = '';


/*** build a select ***/
export
function buildSelect(name: string,
                     list: string[],
                     def?: string,
                     required = false,
                     readonly = false): HTMLSelectElement {
  let select = document.createElement('select');
  select.name = name;
  if(required){
    select.required = required;
  }
  if(readonly){
    select.disabled = true;
  }

  select.appendChild(default_none);
  for(let i=0; i<list.length; i++) {
    let x = list[i];
    let option = document.createElement('option');
    option.value = x
    option.textContent = x;
    select.appendChild(option);

    if (def && x === def){
      option.selected = true;
    }
  }
  select.style.marginBottom = '15px';
  select.style.minHeight = '25px';
  return select;
}
