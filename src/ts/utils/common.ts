/*** Title Case formatter ***/
export
function toProperCase(str: string) {
  return str.replace(/\w\S*/g,
    (txt: string) => {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    },
  );
}
