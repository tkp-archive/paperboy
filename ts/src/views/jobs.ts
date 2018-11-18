import {PrimaryTab} from './common';
import {Status} from './status';

export
class Jobs extends PrimaryTab {
    constructor(status: Status){
        super('scheduler', 'jobs', status);
    }
}
