import {
    Widget
} from '@phosphor/widgets';

import {request, RequestResult} from './request';



export
class Status extends Widget {
    static createNode(): HTMLElement {
        let node = document.createElement('div');
        node.classList.add('status');
        return node;
    }

    static createSubtitle(clazz: string, title: string, data: any) : HTMLDivElement {
        let sec = document.createElement('div');
        sec.classList.add('status-' + clazz);

        let sec_sp = document.createElement('span');
        sec_sp.classList.add('number');
        sec_sp.classList.add(clazz);
        let sec_sp2 = document.createElement('span');


        sec_sp.textContent = data.json()[clazz];
        sec_sp2.textContent = title;
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

        let sec_sp2 = document.createElement('span');
        sec_sp2.textContent = data.json()[clazz];

        sec.appendChild(sec_sp);
        sec.appendChild(sec_sp2);
    }

    private populateTop(data: any): void {
        this.top.classList.add('status-container');

        let nb = Status.createSubtitle('notebooks', 'Notebooks', data);
        let jb = Status.createSubtitle('jobs', 'Jobs', data);
        let rp = Status.createSubtitle('reports', 'Reports', data);

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
            this.populateTop(res);
        });

        request('get', '/api/v1/notebooks').then((res: RequestResult) => {
            Status.createSubsection(this.nbs, 'notebooks', 'Notebooks', res);
        });

        request('get', '/api/v1/jobs').then((res: RequestResult) => {
            Status.createSubsection(this.jbs, 'jobs', 'Jobs', res);
        });

        request('get', '/api/v1/reports').then((res: RequestResult) => {
            Status.createSubsection(this.rps, 'reports', 'Reports', res);
        });
    }

    private top = document.createElement('div');
    private nbs = document.createElement('div');
    private jbs = document.createElement('div');
    private rps = document.createElement('div');
}
