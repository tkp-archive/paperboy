import {
    Widget, TabPanel, BoxPanel
} from '@phosphor/widgets';

import {request, RequestResult} from './request';



export
class Browser extends TabPanel {
    static createSubsection(sec: BoxPanel, clazz: string, data: any) : void {
        let page = data['page'];
        let pages = data['pages'];
        let count = data['count'];
        let total = data['total'];

        let notebooks = data[clazz];

        let table = document.createElement('table');

        let row = document.createElement('tr');
        let name = document.createElement('th');
        name.textContent = 'Name';
        row.appendChild(name);
        table.appendChild(row);

        for(let nb of notebooks){
            row = document.createElement('tr');

            let v = document.createElement('td');
            v.textContent = nb['name'];
            row.appendChild(v);
            table.appendChild(row);
        }

        let p1 = document.createElement('p');
        p1.textContent = 'Showing ' + count + ' of ' + total;

        let p2 = document.createElement('p');
        for(let i = 1; i <= pages; i++){
            let span = document.createElement('span');
            span.textContent = i + ' ';
            if (i === page){
                span.classList.add('page-active');
            }
            span.classList.add('page');
            p2.appendChild(span);
        }

        sec.node.appendChild(table);
        sec.node.appendChild(p1);
        sec.node.appendChild(p2);
    }

    constructor(){
        super();
        this.nbs = new BoxPanel();
        this.nbs.title.label = 'Notebooks';
        this.nbs.node.classList.add('browser-container');

        this.jbs = new BoxPanel();
        this.jbs.title.label = 'Jobs';
        this.jbs.node.classList.add('browser-container');

        this.rps = new BoxPanel();
        this.rps.title.label = 'Reports';
        this.rps.node.classList.add('browser-container');

        this.addWidget(this.nbs);
        this.addWidget(this.jbs);
        this.addWidget(this.rps);

        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
        this.node.id = 'browser';
        this.node.classList.add('browser');

        request('get', '/api/v1/notebooks').then((res: RequestResult) => {
            Browser.createSubsection(this.nbs, 'notebooks', res.json());
        });
        request('get', '/api/v1/jobs').then((res: RequestResult) => {
            Browser.createSubsection(this.jbs, 'jobs', res.json());
        });
        request('get', '/api/v1/reports').then((res: RequestResult) => {
            Browser.createSubsection(this.rps, 'reports', res.json());
        });
    }

    private nbs: BoxPanel;
    private jbs: BoxPanel;
    private rps: BoxPanel;
}
