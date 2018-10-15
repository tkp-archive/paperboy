import {
    Widget, DockPanel, BoxPanel
} from '@phosphor/widgets';

import {request, RequestResult} from './request';
import {DomUtils} from './utils';

class Scheduler extends Widget {
    static createNode(): HTMLDivElement {
        let div = document.createElement('div');
        div.classList.add('scheduler');

        div.appendChild(DomUtils.buildLabel('Notebook'));
        div.appendChild(DomUtils.buildSelect(['Test1', 'Test2', 'Test3']));

        return div;
    }

    constructor(){
        super({node: Scheduler.createNode()});
        this.title.closable = false;
        this.title.label = 'Scheduler';
    }
}

export
class Jobs extends DockPanel {
    constructor(){
        super();
        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.label = 'Jobs';
        this.node.id = 'jobs';
        this.node.classList.add('jobs');

        this.mine.title.closable = false;
        this.mine.title.label = 'My Jobs';

        request('get', '/api/v1/jobs').then((res: RequestResult) => {
            DomUtils.createSubsection(this.mine, 'jobs', res.json());
        });
        this.addWidget(this.mine);
        this.addWidget(new Scheduler(), {mode: 'tab-after', ref: this.mine});
    }

    private mine = new BoxPanel();
}
