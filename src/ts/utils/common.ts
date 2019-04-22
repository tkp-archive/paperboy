/*** Title Case formatter ***/
/**
 *
 * @param str string to be converted to TitleCase
 * @returns string in TitleCase
 */
export
function toProperCase(str: string): string {
  return str.replace(/\w\S*/g,
    (txt: string) => {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    },
  );
}
