import {PrimaryTab} from './common';
import {Status} from './status';

export
class Notebooks extends PrimaryTab {
    constructor(status: Status){
        super('uploader', 'notebooks', status);
    }
}
