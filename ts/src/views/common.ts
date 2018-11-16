import {
    Widget, DockPanel, BoxPanel
} from '@phosphor/widgets';

import {request, RequestResult} from '../utils/request';
import {toProperCase, apiurl, createDetail, createConfigForm, createPrimarySection} from '../utils/index';


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

    constructor(clz: string, type: string, detail: PrimaryTab){
        super({node: PrimaryForm.createNode(clz)});
        this.title.closable = false;
        this.title.label = toProperCase(clz);
        request('get', apiurl() + 'config?type=' + type).then((res: RequestResult) => {
            createConfigForm(this.node.querySelector('form'), type, res.json(),
                () => {detail.update();});
        });
    }
    clz: string;
    type: string;
}


export
class PrimaryDetail extends Widget {
    static createNode(type: string): HTMLElement {
        let div = document.createElement('div');
        div.classList.add('details');
        div.classList.add(type + '-detail');
        return div;
    }

    constructor(type: string, id: string){
        super({node: PrimaryDetail.createNode(type)});
        this.type = type;
        this.title.closable = true;
        this.request = apiurl() + this.type + '/details?id=' + id;
        this.update();
    }

    update(): void {
        request('get', this.request).then((res: RequestResult) => {
            let dat = res.json() as any;
            createDetail(dat, this.title, this.node);
        });
    }

    type: string;
    request: string;
}

export
class PrimaryTab extends DockPanel {
    constructor(clz: string, type: string){
        super();
        this.clz = clz;
        this.type = type;

        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.label = toProperCase(type);
        this.node.id = type;
        this.mine.node.classList.add('primary');
        this.node.classList.add(type);

        this.mine.title.closable = false;
        this.mine.title.label = this.title.label;
        this.request = apiurl() + type;

        this.update();
        this.control = this.controlView();

        this.addWidget(this.mine);
        this.addWidget(this.control, {mode: 'tab-after', ref: this.mine});
    }

    update(): void {
        request('get', this.request).then((res: RequestResult) => {

            createPrimarySection(this, this.type, res.json(),
                (page: number) => {
                    this.request = apiurl() + this.type + '?page=' + page;
                    this.update();
               });
        });
    }

    controlView(): PrimaryForm {
        return new PrimaryForm(this.clz, this.type, this);
    }

    detailView(id: string): void {
        let pd = new PrimaryDetail(this.type, id);
        this.addWidget(pd);
        this.selectWidget(pd);
    }

    clz: string;
    type: string;
    request: string;
    mine = new BoxPanel();
    control: PrimaryForm;
}
