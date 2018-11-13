import {
    Widget, TabPanel, BoxPanel, SplitPanel
} from '@phosphor/widgets';

import {request, RequestResult} from './request';
import {toProperCase, apiurl, DomUtils} from './utils';


export
class StatusBrowser extends TabPanel {
    constructor(){
        super();
        this.jbs = new BoxPanel();
        this.jbs.title.label = 'Jobs';
        this.jbs.node.classList.add('schedulerbrowser-container');

        this.rps = new BoxPanel();
        this.rps.title.label = 'Reports';
        this.rps.node.classList.add('schedulerbrowser-container');

        this.addWidget(this.jbs);
        this.addWidget(this.rps);

        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
        this.node.id = 'schedulerbrowser';
        this.node.classList.add('schedulerbrowser');

        request('get', apiurl() + 'scheduler?type=jobs').then((res: RequestResult) => {
            DomUtils.createStatusSection(this.jbs, 'jobs', res.json());
        });
        request('get', apiurl() + 'scheduler?type=reports').then((res: RequestResult) => {
            DomUtils.createStatusSection(this.rps, 'reports', res.json());
        });

        setInterval(() => {
            request('get', apiurl() + 'scheduler?type=jobs').then((res: RequestResult) => {
                if(!res.url.includes(apiurl() + 'scheduler?type=jobs')){
                  window.location.href = (document as any).loginurl;
                }
                DomUtils.delete_all_children(this.jbs.node);
                DomUtils.createStatusSection(this.jbs, 'jobs', res.json());
            });
        }, 10000);

        setInterval(() => {
            request('get', apiurl() + 'scheduler?type=reports').then((res: RequestResult) => {
                if(!res.url.includes(apiurl() + 'scheduler?type=reports')){
                  window.location.href = (document as any).loginurl;
                }
                DomUtils.delete_all_children(this.rps.node);
                DomUtils.createStatusSection(this.rps, 'reports', res.json());
            });
        }, 10000);
    }

    private jbs: BoxPanel;
    private rps: BoxPanel;
}


export
class StatusOverview extends Widget {
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
            v.classList.add('status-data');

            row.appendChild(k);
            row.appendChild(v);
            table.appendChild(row);
        }
        sec.appendChild(table);
    }

    private populateTop(data: any): void {
        this.top.classList.add('status-container');

        let nb = StatusOverview.createSubtitle('notebooks', data);
        let jb = StatusOverview.createSubtitle('jobs', data);
        let rp = StatusOverview.createSubtitle('reports', data);

        this.top.appendChild(nb);
        this.top.appendChild(jb);
        this.top.appendChild(rp);
    }

    constructor(){
        super({ node: StatusOverview.createNode() });
        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
        this.node.id = 'status';

        this.node.appendChild(this.top);
        this.node.appendChild(this.nbs);
        this.node.appendChild(this.jbs);
        this.node.appendChild(this.rps);

        request('get', apiurl() + 'status').then((res: RequestResult) => {
            let data = res.json()
            this.populateTop(data);
            StatusOverview.createSubsection(this.nbs, 'notebooks', 'Notebooks', data);
            StatusOverview.createSubsection(this.jbs, 'jobs', 'Jobs', data);
            StatusOverview.createSubsection(this.rps, 'reports', 'Reports', data);
        });
    }

    private top = document.createElement('div');
    private nbs = document.createElement('div');
    private jbs = document.createElement('div');
    private rps = document.createElement('div');
}



export
class Status extends SplitPanel {
    constructor(){
        super({ orientation: 'vertical'});
        this.addWidget(new StatusOverview());
        this.addWidget(new StatusBrowser());
        this.setRelativeSizes([.5, .5]);
    }
}