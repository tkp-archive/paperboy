import {
    Widget
} from '@phosphor/widgets';

import {request, RequestResult} from './request';
import {toProperCase} from './utils';

export
class Status extends Widget {
    static createNode(): HTMLElement {
        let node = document.createElement('div');
        node.classList.add('status');
        return node;
    }

    static createSubtitle(clazz: string, data: any) : HTMLDivElement {
        let sec = document.createElement('div');
        sec.classList.add('status-' + clazz);

        let sec_sp = document.createElement('span');
        sec_sp.classList.add('number');
        sec_sp.classList.add(clazz);
        let sec_sp2 = document.createElement('span');


        sec_sp.textContent = data[clazz]['total'];
        sec_sp2.textContent = toProperCase(clazz);
        sec.appendChild(sec_sp);
        sec.appendChild(sec_sp2);
        return sec;
    }

    static createSubsection(sec: HTMLDivElement, clazz: string, title: string, data: any) : void {
        sec.classList.add('status-breakdown');

        let sec_sp = document.createElement('span');
        sec_sp.classList.add('subtitle');
        sec_sp.classList.add(clazz);
        sec_sp.textContent = title;

        sec.appendChild(sec_sp);

        let table = document.createElement('table');
        data = data[clazz];
        for(let section of Object.keys(data)){
            let row = document.createElement('tr');
            let k = document.createElement('td');
            let v = document.createElement('td');

            k.textContent = toProperCase(section);
            v.textContent = data[section];
            row.appendChild(k);
            row.appendChild(v);
            table.appendChild(row);
        }
        sec.appendChild(table);
    }

    private populateTop(data: any): void {
        this.top.classList.add('status-container');

        let nb = Status.createSubtitle('notebooks', data);
        let jb = Status.createSubtitle('jobs', data);
        let rp = Status.createSubtitle('reports', data);

        this.top.appendChild(nb);
        this.top.appendChild(jb);
        this.top.appendChild(rp);
    }

    constructor(){
        super({ node: Status.createNode() });
        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
        this.node.id = 'status';

        this.node.appendChild(this.top);
        this.node.appendChild(this.nbs);
        this.node.appendChild(this.jbs);
        this.node.appendChild(this.rps);

        request('get', '/api/v1/status').then((res: RequestResult) => {
            let data = res.json()
            this.populateTop(data);
            Status.createSubsection(this.nbs, 'notebooks', 'Notebooks', data);
            Status.createSubsection(this.jbs, 'jobs', 'Jobs', data);
            Status.createSubsection(this.rps, 'reports', 'Reports', data);
        });
    }

    private top = document.createElement('div');
    private nbs = document.createElement('div');
    private jbs = document.createElement('div');
    private rps = document.createElement('div');
}
