import {buildLabel} from "./label";

// tslint:disable: no-empty

/**
 * Helper utility to build generic dom nodes from server's json responses
 * @param type type of element to build, usually a dom type
 * @param content text content of element
 * @param name name of element
 */
export
function buildGeneric(type: string, content?: string, name?: string): HTMLElement {
  switch (type) {
    /* Basic types are trivial, create the type and fill text content */
    case "br": {}
    case "span": {}
    case "p": {}
    case "button": {}
    case "h1": {}
    case "h2": {}
    case "h3": {}
    case "h4": {}
    case "h5": {}
    case "h6": {
      const d = document.createElement(type);
      d.textContent = content || "";
      return d;
    }
    /* Label has a separate builder */
    case "label": {
      return buildLabel(content || "");
    }
    /* Json we want to wrap it as a download link */
    case "json": {
      const a = document.createElement("a");
      a.download = "download.json";
      a.href = "data:text/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(content));
      a.target = "_blank";
      a.textContent = name || "Download";
      return a;
    }
    /* ipynb we want to wrap as a download link */
    case "ipynb": {
      const a = document.createElement("a");
      a.download = "download.ipynb";
      a.href = "data:text/json;charset=utf-8," +
      JSON.parse(JSON.stringify(content));
      a.target = "_blank";
      a.textContent = name || "Download";
      return a;
    }
    /* text we want to wrap as a download link */
    case "textfile": {
      if (content) {
        const a = document.createElement("a");
        a.download = "download.txt";
        a.href = "data:text/plain;charset=utf-8," + encodeURIComponent(content);
        a.target = "_blank";
        a.textContent = name || "Download";
        return a;
      }
      const s = document.createElement("span");
      s.textContent = "none";
      return s;
    }
    default: {
      return document.createElement("div");
    }
  }
}
