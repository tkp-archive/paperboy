/**
 * Safe baseurl getter
 */
export
function baseurl() {
  return (document as any).baseurl || "/";
}

/**
 * safe apiurl getter
 */
export
function apiurl() {
  return (document as any).apiurl || "/api/v1/";
}
