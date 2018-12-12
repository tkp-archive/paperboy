import {createModal} from './modal';
import {RequestResult} from '../utils/request';

export
function createErrorDialog(res: RequestResult): Promise<void> {
    return new Promise((resolve) => {
        createModal([{'type': 'label', 'value': 'An Error has occurred!'}], true, false).then(() => {
            resolve();
        });
    });
}