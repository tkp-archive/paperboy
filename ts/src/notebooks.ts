import {
    Widget, DockPanel, BoxPanel
} from '@phosphor/widgets';

import {request, RequestResult} from './request';
import {DomUtils} from './utils';


class Uploader extends Widget {
    static createNode(): HTMLElement {
        let div = document.createElement('form');
        div.classList.add('uploader');
        return div;
    }

    constructor(){
        super({node: Uploader.createNode()});
        this.title.closable = false;
        this.title.label = 'Uploader';
        request('get', '/api/v1/config?type=notebooks').then((res: RequestResult) => {
            DomUtils.createConfig(this.node, 'notebooks', res.json());
        });
    }
}

export
class Notebooks extends DockPanel {
    constructor(){
        super();
        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.label = 'Notebooks';
        this.node.id = 'notebooks';
        this.node.classList.add('notebooks');


        this.mine.title.closable = false;
        this.mine.title.label = 'My Notebooks';

        request('get', '/api/v1/notebooks').then((res: RequestResult) => {
            DomUtils.createSubsection(this.mine, 'notebooks', res.json());
        });
        this.addWidget(this.mine);
        this.addWidget(new Uploader(), {mode: 'tab-after', ref: this.mine});
    }

    private mine = new BoxPanel();
}
