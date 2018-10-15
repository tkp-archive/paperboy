import {
    SplitPanel, BoxPanel
} from '@phosphor/widgets';

import {DomUtils, autocomplete} from './utils';


export
class Browser extends SplitPanel {
    constructor(){
        super({ orientation: 'vertical', spacing: 0 });
        this.node.classList.add('browser');


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
                DomUtils.delete_all_children(datalist);
            }

            if (last == search.value){
                // duplicate
                return;
            }

            if (e.keyCode !== 13) {
                autocomplete('/api/v1/autocomplete?partial=' + search.value, search.value, datalist);
            }

            last = search.value;
        };

        search.addEventListener('keyup', foo);
        go.addEventListener('click', () => {
            DomUtils.delete_all_children(datalist);
            if (last == search.value){
                // duplicate
                return;
            }
            autocomplete('/api/v1/autocomplete?partial=' + search.value, search.value, datalist);
            last = search.value;
        });

        holder.appendChild(search);
        holder.appendChild(datalist);
        holder.appendChild(go);

        let searchpanel = new BoxPanel();
        searchpanel.node.appendChild(holder);

        let resultspanel = new BoxPanel();
        this.addWidget(searchpanel);
        this.addWidget(resultspanel);
        this.setRelativeSizes([.3, .7]);
    }
}
