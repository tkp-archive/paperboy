import {PrimaryTab} from './common';
import {Status} from './status';

export
class Notebooks extends PrimaryTab {
    constructor(status: Status){
        super('uploader', 'notebooks', status);
    }
}

export
class Jobs extends PrimaryTab {
    constructor(status: Status){
        super('scheduler', 'jobs', status);
    }
}

export
class Reports extends PrimaryTab {
    constructor(status: Status){
        super('configurator', 'reports', status);
    }
}
