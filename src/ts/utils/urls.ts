export
function baseurl() {
  return (document as any).baseurl || "/";
}

export
function apiurl() {
  return (document as any).apiurl || "/api/v1/";
}
