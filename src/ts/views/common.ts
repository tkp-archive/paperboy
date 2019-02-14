import {
    Widget, Panel, BoxPanel, DockPanel
} from '@phosphor/widgets';

import {request, RequestResult} from '../utils/request';
import {toProperCase, apiurl, createDetail, createConfigForm, createPrimarySection, createErrorDialog} from '../utils/index';
import {Status} from './status';

export
class PrimaryForm extends Widget {
    static createNode(clz: string): HTMLElement {
        let div = document.createElement('div');
        div.classList.add(clz);
        let form = document.createElement('form');
        form.enctype = 'multipart/form-data';
        div.appendChild(form);
        return div;
    }

    constructor(clz: string, type: string, primary: PrimaryTab, status: Status){
        super({node: PrimaryForm.createNode(clz)});
        this.title.closable = true;
        this.title.label = toProperCase(clz);
        this.type = type;
        this.primary = primary;
        this.status = status;
        this.update();
    }

    update(): void {
        request('get', apiurl() + 'config?type=' + this.type).then((res: RequestResult) => {
            if(res.ok){
                createConfigForm(this.node.querySelector('form'), this.type, res.json(),
                    () => {
                        this.primary.update();
                        this.status.update();
                    }
                );
            } else {
                createErrorDialog(res);
            }
        });
    }
    clz: string;
    type: string;
    primary: PrimaryTab;
    status: Status;
}


export
class PrimaryDetail extends Widget {
    constructor(type: string, id: string, primary: PrimaryTab, status: Status){
        //create dom elements
        let div = document.createElement('div');
        div.classList.add('details');
        div.classList.add(type + '-detail');
        let form = document.createElement('form');
        form.enctype = 'multipart/form-data';
        div.appendChild(form);

        super({node: div});
        this.form = form;
        this.type = type;
        this.title.closable = true;

        this.request = apiurl() + this.type + '/details?id=' + id;
        this.primary = primary;
        this.status = status;
        this.update();
    }

    update(): void {
        request('get', this.request).then((res: RequestResult) => {
            if(res.ok){
                let dat = res.json() as any;
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

    type: string;
    request: string;
    form: HTMLFormElement;
    primary: PrimaryTab;
    status: Status;
}

export
class PrimaryTab extends Panel {
    constructor(clz: string, type: string, status: Status, parent: DockPanel){
        super();
        this.clz = clz;
        this.type = type;
        this.status = status;

        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.label = toProperCase(type);
        this.title.closable = true;

        this.node.id = type;
        this.mine.node.classList.add('primary');
        this.node.classList.add(type);

        this.mine.title.closable = true;
        this.mine.title.label = this.title.label;
        this.request = apiurl() + type;

        this.parent = parent;
        this.control = this.controlView();
        this.update();
        this.addWidget(this.mine);
    }

    update(): void {
        request('get', this.request).then((res: RequestResult) => {
            if(res.ok){
                createPrimarySection(this, this.type, res.json(),
                    (page: number) => {
                        this.request = apiurl() + this.type + '?page=' + page;
                        this.update();
               });
            } else {
                createErrorDialog(res);
            }
        });
    }

    controlView(): PrimaryForm {
        return new PrimaryForm(this.clz, this.type, this, this.status);
    }

    detailView(id: string): void {
        let pd = new PrimaryDetail(this.type, id, this, this.status);
        this.parent.addWidget(pd);
        this.parent.selectWidget(pd);
    }

    clz: string;
    type: string;
    request: string;

    parent: DockPanel;
    mine = new BoxPanel();
    control: PrimaryForm;
    status: Status;
}
