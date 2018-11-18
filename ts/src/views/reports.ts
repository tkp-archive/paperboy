import {PrimaryTab} from './common';
import {Status} from './status';

export
class Reports extends PrimaryTab {
    constructor(status: Status){
        super('configurator', 'reports', status);
    }
}
