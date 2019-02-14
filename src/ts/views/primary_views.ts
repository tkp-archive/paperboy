import {DockPanel} from '@phosphor/widgets';
import {PrimaryTab} from './common';
import {Status} from './status';

export
class Notebooks extends PrimaryTab {
    constructor(home: DockPanel, status: Status){
        super('uploader', 'notebooks', status, home);
    }
}

export
class Jobs extends PrimaryTab {
    constructor(home: DockPanel, status: Status){
        super('scheduler', 'jobs', status, home);
    }
}

export
class Reports extends PrimaryTab {
    constructor(home: DockPanel, status: Status){
        super('configurator', 'reports', status, home);
    }
}
