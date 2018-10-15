import {
    SplitPanel, BoxPanel
} from '@phosphor/widgets';

import {request, RequestResult} from './request';
import {DomUtils} from './utils';


function autocomplete_ticker(path: string, value: string, autocomplete: HTMLDataListElement){
    request('get', '/api/v1/autocomplete').then((res: RequestResult) => {
        var jsn = <any>res.json();
        if (jsn) {
            DomUtils.delete_all_children(autocomplete);

            for(let val of jsn){
                let option = document.createElement('option');
                option.value = val['key'];
                option.innerText = val['key'] + ' - ' + val['name'];
                autocomplete.appendChild(option);
            }
        }
    });
}

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
                autocomplete_ticker('/api/v1/autocomplete?partial=' + search.value, search.value, datalist);
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
            autocomplete_ticker('/api/v1/autocomplete?partial=' + search.value, search.value, datalist);
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
