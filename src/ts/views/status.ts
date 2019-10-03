import {
    BoxPanel, SplitPanel, TabPanel, Widget,
} from "@phosphor/widgets";

import {IRequestResult, request} from "requests-helper";
import {createStatusSection } from "../utils/components/index";
import {deleteAllChildren} from "../utils/dom/index";
import {apiurl, createErrorDialog, toProperCase} from "../utils/index";

export
class StatusBrowser extends TabPanel {

    private jbs: BoxPanel;
    private rps: BoxPanel;
    constructor() {
        super();
        this.jbs = new BoxPanel();
        this.jbs.title.label = "Jobs";
        this.jbs.node.classList.add("schedulerbrowser-container");

        this.rps = new BoxPanel();
        this.rps.title.label = "Reports";
        this.rps.node.classList.add("schedulerbrowser-container");

        this.addWidget(this.jbs);
        this.addWidget(this.rps);

        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = true;
        this.node.id = "schedulerbrowser";
        this.node.classList.add("schedulerbrowser");

        request("get", apiurl() + "scheduler?type=jobs").then((res: IRequestResult) => {
            createStatusSection(this.jbs, "jobs", res.json());
        });
        request("get", apiurl() + "scheduler?type=reports").then((res: IRequestResult) => {
            if (res.ok) {
                createStatusSection(this.rps, "reports", res.json());
            } else {
                createErrorDialog(res);
            }
        });

        setInterval(() => {
            request("get", apiurl() + "scheduler?type=jobs").then((res: IRequestResult) => {
                if (!res.url.includes(apiurl() + "scheduler?type=jobs")) {
                  window.location.href = (document as any).loginurl;
                }
                deleteAllChildren(this.jbs.node);
                createStatusSection(this.jbs, "jobs", res.json());
            });
        }, 10000);

        setInterval(() => {
            request("get", apiurl() + "scheduler?type=reports").then((res: IRequestResult) => {
                if (!res.url.includes(apiurl() + "scheduler?type=reports")) {
                  window.location.href = (document as any).loginurl;
                }
                deleteAllChildren(this.rps.node);
                createStatusSection(this.rps, "reports", res.json());
            });
        }, 10000);
    }

    // tslint:disable-next-line: no-empty
    public update(): void {

    }
}

// tslint:disable-next-line: max-classes-per-file
export
class StatusOverview extends Widget {
    public static createNode(): HTMLElement {
        const node = document.createElement("div");
        node.classList.add("status");
        return node;
    }

    public static createSubtitle(clazz: string, data: any): HTMLDivElement {
        const sec = document.createElement("div");
        sec.classList.add("status-" + clazz);

        const secSp = document.createElement("span");
        secSp.classList.add("number");
        secSp.classList.add(clazz);
        const secSp2 = document.createElement("span");

        secSp.textContent = data[clazz].total;
        secSp2.textContent = toProperCase(clazz);
        sec.appendChild(secSp);
        sec.appendChild(secSp2);
        return sec;
    }

    public static createSubsection(sec: HTMLDivElement, clazz: string, title: string, data: any): void {
        sec.classList.add("status-breakdown");
        deleteAllChildren(sec);

        const secSp = document.createElement("span");
        secSp.classList.add("subtitle");
        secSp.classList.add(clazz);
        secSp.textContent = title;

        sec.appendChild(secSp);

        const table = document.createElement("table");
        data = data[clazz];
        for (const section of Object.keys(data)) {
            const row = document.createElement("tr");
            const k = document.createElement("td");
            const v = document.createElement("td");

            k.textContent = toProperCase(section);
            v.textContent = data[section];
            v.classList.add("status-data");

            row.appendChild(k);
            row.appendChild(v);
            table.appendChild(row);
        }
        sec.appendChild(table);
    }

    private top = document.createElement("div");
    private nbs = document.createElement("div");
    private jbs = document.createElement("div");
    private rps = document.createElement("div");

    constructor() {
        super({ node: StatusOverview.createNode() });
        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
        this.node.id = "status";

        this.node.appendChild(this.top);
        this.node.appendChild(this.nbs);
        this.node.appendChild(this.jbs);
        this.node.appendChild(this.rps);
        this.update();
    }

    public update(): void {
        request("get", apiurl() + "status").then((res: IRequestResult) => {
            if (res.ok) {
                const data = res.json();
                this.populateTop(data);
                StatusOverview.createSubsection(this.nbs, "notebooks", "Notebooks", data);
                StatusOverview.createSubsection(this.jbs, "jobs", "Jobs", data);
                StatusOverview.createSubsection(this.rps, "reports", "Reports", data);
            } else {
                createErrorDialog(res);
            }
        });
    }

    private populateTop(data: any): void {
        this.top.classList.add("status-container");
        deleteAllChildren(this.top);

        const nb = StatusOverview.createSubtitle("notebooks", data);
        const jb = StatusOverview.createSubtitle("jobs", data);
        const rp = StatusOverview.createSubtitle("reports", data);

        this.top.appendChild(nb);
        this.top.appendChild(jb);
        this.top.appendChild(rp);
    }
}

// tslint:disable-next-line: max-classes-per-file
export
class Status extends SplitPanel {

    public overview: StatusOverview;
    public browser: StatusBrowser;
    constructor() {
        super({ orientation: "horizontal"});
        this.overview = new StatusOverview();
        this.browser = new StatusBrowser();
        this.addWidget(this.overview);
        this.addWidget(this.browser);
        this.setRelativeSizes([.4, .6]);
        this.title.label = "Status";
        this.title.closable = true;
    }

    public update(): void {
        this.overview.update();
        this.browser.update();
    }
}
