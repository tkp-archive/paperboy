import {
    BoxPanel, DockPanel, Panel, Widget,
} from "@phosphor/widgets";

import {apiurl,
        createConfigForm,
        createDetail,
        createErrorDialog,
        createPrimarySection,
        toProperCase} from "../utils/index";
import {IRequestResult, request} from "../utils/request";
import {Status} from "./status";

export
class PrimaryForm extends Widget {
    public static createNode(clz: string): HTMLElement {
        const div = document.createElement("div");
        div.classList.add(clz);
        const form = document.createElement("form");
        form.enctype = "multipart/form-data";
        div.appendChild(form);
        return div;
    }
    public clz: string;
    public type: string;
    public primary: PrimaryTab;
    public status: Status;

    constructor(clz: string, type: string, primary: PrimaryTab, status: Status) {
        super({node: PrimaryForm.createNode(clz)});
        this.title.closable = true;
        this.title.label = toProperCase(clz);
        this.type = type;
        this.primary = primary;
        this.status = status;
        this.update();
    }

    public update(): void {
        request("get", apiurl() + "config?type=" + this.type).then((res: IRequestResult) => {
            if (res.ok) {
                createConfigForm(this.node.querySelector("form"), this.type, res.json(),
                    () => {
                        this.primary.update();
                        this.status.update();
                    },
                );
            } else {
                createErrorDialog(res);
            }
        });
    }
}

// tslint:disable-next-line: max-classes-per-file
export
class PrimaryDetail extends Widget {

    public type: string;
    public request: string;
    public form: HTMLFormElement;
    public primary: PrimaryTab;
    public status: Status;
    constructor(type: string, id: string, primary: PrimaryTab, status: Status) {
        // create dom elements
        const div = document.createElement("div");
        div.classList.add("details");
        div.classList.add(type + "-detail");
        const form = document.createElement("form");
        form.enctype = "multipart/form-data";
        div.appendChild(form);

        super({node: div});
        this.form = form;
        this.type = type;
        this.title.closable = true;

        this.request = apiurl() + this.type + "/details?id=" + id;
        this.primary = primary;
        this.status = status;
        this.update();
    }

    public update(): void {
        request("get", this.request).then((res: IRequestResult) => {
            if (res.ok) {
                const dat = res.json() as any;
                createDetail(this.form, this.title, dat).then(() => {
                    this.primary.update();
                    this.status.update();
                    this.close();
                });
            } else {
                createErrorDialog(res);
            }
        });
    }
}

// tslint:disable-next-line: max-classes-per-file
export
class PrimaryTab extends Panel {

    public clz: string;
    public type: string;
    public request: string;

    public parent: DockPanel;
    public mine = new BoxPanel();
    public control: PrimaryForm;
    public status: Status;
    constructor(clz: string, type: string, status: Status, parent: DockPanel) {
        super();
        this.clz = clz;
        this.type = type;
        this.status = status;

        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.label = toProperCase(type);
        this.title.closable = true;

        this.node.id = type;
        this.mine.node.classList.add("primary");
        this.node.classList.add(type);

        this.mine.title.closable = true;
        this.mine.title.label = this.title.label;
        this.request = apiurl() + type;

        this.parent = parent;
        this.control = this.controlView();
        this.update();
        this.addWidget(this.mine);
    }

    public update(): void {
        request("get", this.request).then((res: IRequestResult) => {
            if (res.ok) {
                createPrimarySection(this, this.type, res.json(),
                    (page: number) => {
                        this.request = apiurl() + this.type + "?page=" + page;
                        this.update();
               });
            } else {
                createErrorDialog(res);
            }
        });
    }

    public controlView(): PrimaryForm {
        return new PrimaryForm(this.clz, this.type, this, this.status);
    }

    public detailView(id: string): void {
        const pd = new PrimaryDetail(this.type, id, this, this.status);
        this.parent.addWidget(pd);
        this.parent.selectWidget(pd);
    }
}

// tslint:disable-next-line: max-classes-per-file
export
class Notebooks extends PrimaryTab {
    constructor(home: DockPanel, status: Status) {
        super("uploader", "notebooks", status, home);
    }
}

// tslint:disable-next-line: max-classes-per-file
export
class Jobs extends PrimaryTab {
    constructor(home: DockPanel, status: Status) {
        super("scheduler", "jobs", status, home);
    }
}

// tslint:disable-next-line: max-classes-per-file
export
class Reports extends PrimaryTab {
    constructor(home: DockPanel, status: Status) {
        super("configurator", "reports", status, home);
    }
}
