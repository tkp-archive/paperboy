import {
    SplitPanel, BoxPanel, DockPanel
} from '@phosphor/widgets';

import {deleteAllChildren, autocomplete, apiurl, showLoader, hideLoader} from '../utils/index';
import {PrimaryDetail} from './common';

export
class Browser extends SplitPanel {
    constructor(){
        super({ orientation: 'vertical', spacing: 0 });
        this.node.classList.add('browser');
        let searchpanel = new BoxPanel();
        let resultspanel = new DockPanel();

        let holder = document.createElement('div');
        holder.classList.add('search-holder');

        let search = document.createElement('input');
        search.setAttribute('list', 'browser-datalist');
        search.placeholder = 'Search...';

        let datalist = document.createElement('datalist');
        datalist.id = 'browser-datalist';

        let go = document.createElement('button');
        go.textContent = 'Go';

        let last = '';

        let foo = (e: KeyboardEvent) => {
            if (e.keyCode === 13){
                deleteAllChildren(datalist);
            }

            if (last == search.value){
                // duplicate
                return;
            }

            if (e.keyCode !== 13) {
                autocomplete(apiurl() + 'autocomplete?partial=' + search.value, search.value, datalist);
            }

            last = search.value;
        };

        search.addEventListener('keyup', foo);
        go.addEventListener('click', () => {
            deleteAllChildren(datalist);
            if (last == search.value){
                // duplicate
            } else {
                autocomplete(apiurl() + 'autocomplete?partial=' + search.value, search.value, datalist);
                last = search.value;
            }
            let type;
            if(search.value.toLowerCase().startsWith('notebook-')){
                type = 'notebooks';
            }else if(search.value.toLowerCase().startsWith('job-')){
                type = 'jobs';
            }else if(search.value.toLowerCase().startsWith('report-')){
                type = 'reports';
            } else {
                type = '';
            }
            showLoader();
            resultspanel.addWidget(new PrimaryDetail(type, search.value));
            hideLoader();
        });

        holder.appendChild(search);
        holder.appendChild(datalist);
        holder.appendChild(go);
        searchpanel.node.appendChild(holder);

        this.addWidget(searchpanel);
        this.addWidget(resultspanel);
        this.setRelativeSizes([.2, .8]);
    }
}
