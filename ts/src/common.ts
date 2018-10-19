import {
    Widget, DockPanel, BoxPanel
} from '@phosphor/widgets';

import {request, RequestResult} from './request';
import {toProperCase, DomUtils, apiurl} from './utils';


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

    constructor(clz: string, type: string){
        super({node: PrimaryForm.createNode(clz)});
        this.title.closable = false;
        this.title.label = toProperCase(clz);
        request('get', apiurl() + 'config?type=' + type).then((res: RequestResult) => {
            DomUtils.createConfig(this.node.querySelector('form'), type, res.json());
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

        request('get', apiurl() + this.type + '/details?id=' + id).then((res: RequestResult) => {
            let dat = res.json() as any;

            let table = document.createElement('table');

            for(let i=0; i<dat.length; i++){
                let row = document.createElement('tr');
                let td1 = document.createElement('td');
                let td2 = document.createElement('td');
                if(dat[i]['name'] === 'name'){
                    this.title.label = dat[i]['value'];
                }

                td1.textContent = toProperCase(dat[i]['name']);

                let conts;
                if(dat[i]['type'] == 'select'){
                    conts = DomUtils.buildSelect(dat[i]['name'],
                        dat[i]['options'],
                        '',
                        dat[i]['required'],
                        dat[i]['readonly']);
                } else {
                    conts = DomUtils.buildInput(dat[i]['type'], 
                        dat[i]['name'],
                        dat[i]['placeholder'],
                        dat[i]['value'],
                        dat[i]['required'],
                        dat[i]['readonly']);
                }

                td2.appendChild(conts);

                row.appendChild(td1);
                row.appendChild(td2);
                table.appendChild(row);
            }
            this.node.appendChild(table);
        });
    }

    type: string;
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
        this.node.classList.add('primary');
        this.node.classList.add(type);

        this.mine.title.closable = false;
        this.mine.title.label = 'My ' + this.title.label;

        request('get', apiurl() + type).then((res: RequestResult) => {
            DomUtils.createPrimarySection(this, type, res.json());
        });

        this.control = this.controlView();

        this.addWidget(this.mine);
        this.addWidget(this.control, {mode: 'tab-after', ref: this.mine});
    }

    controlView(): PrimaryForm {
        return new PrimaryForm(this.clz, this.type);
    }

    detailView(id: string): void {
        this.addWidget(new PrimaryDetail(this.type, ''));
    }

    clz: string;
    type: string;
    mine = new BoxPanel();
    control: PrimaryForm;
}
