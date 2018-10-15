import {
    Widget, TabPanel, BoxPanel
} from '@phosphor/widgets';

import {request, RequestResult} from './request';
import {DomUtils} from './utils';


export
class QuickBrowser extends TabPanel {
    constructor(){
        super();
        this.nbs = new BoxPanel();
        this.nbs.title.label = 'Notebooks';
        this.nbs.node.classList.add('quickbrowser-container');

        this.jbs = new BoxPanel();
        this.jbs.title.label = 'Jobs';
        this.jbs.node.classList.add('quickbrowser-container');

        this.rps = new BoxPanel();
        this.rps.title.label = 'Reports';
        this.rps.node.classList.add('quickbrowser-container');

        this.addWidget(this.nbs);
        this.addWidget(this.jbs);
        this.addWidget(this.rps);

        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
        this.node.id = 'quickbrowser';
        this.node.classList.add('quickbrowser');

        request('get', '/api/v1/notebooksqb').then((res: RequestResult) => {
            DomUtils.createSubsection(this.nbs, 'notebooks', res.json());
        });
        request('get', '/api/v1/jobsqb').then((res: RequestResult) => {
            DomUtils.createSubsection(this.jbs, 'jobs', res.json());
        });
        request('get', '/api/v1/reportsqb').then((res: RequestResult) => {
            DomUtils.createSubsection(this.rps, 'reports', res.json());
        });
    }

    private nbs: BoxPanel;
    private jbs: BoxPanel;
    private rps: BoxPanel;
}
