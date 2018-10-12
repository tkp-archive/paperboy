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

    private populateNode(data: any): void {
        let nb = document.createElement('div');
        nb.classList.add('status-notebooks');
        let nb_sp = document.createElement('span');
        nb_sp.classList.add('number');
        nb_sp.classList.add('notebooks');
        let nb_sp2 = document.createElement('span');
        nb_sp.textContent = data.json()['notebooks'];
        nb_sp2.textContent = 'Notebooks';
        nb.appendChild(nb_sp);
        nb.appendChild(nb_sp2);

        let jb = document.createElement('div');
        jb.classList.add('status-jobs');
        let jb_sp = document.createElement('span');
        jb_sp.classList.add('number');
        jb_sp.classList.add('jobs');
        let jb_sp2 = document.createElement('span');
        jb_sp.textContent = data.json()['jobs'];
        jb_sp2.textContent = 'Jobs';
        jb.appendChild(jb_sp);
        jb.appendChild(jb_sp2);

        let rp = document.createElement('div');
        rp.classList.add('status-reports');
        let rp_sp = document.createElement('span');
        rp_sp.classList.add('number');
        rp_sp.classList.add('reports');
        let rp_sp2 = document.createElement('span');
        rp_sp.textContent = data.json()['reports'];
        rp_sp2.textContent = 'Reports';
        rp.appendChild(rp_sp);
        rp.appendChild(rp_sp2);

        this.node.appendChild(nb);
        this.node.appendChild(jb);
        this.node.appendChild(rp);
    }

    constructor(){
        super({ node: Status.createNode() });
        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
        this.node.id = 'status';

        request('get', '/api/v1/status').then((res: RequestResult) => {
            this.populateNode(res);
        });
    }
}
