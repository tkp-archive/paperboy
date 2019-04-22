import {IRequestResult} from "../request";
import {createModal} from "./modal";

/**
 * Helper function to create an error modal
 * @param res failed request response details
 */
export
function createErrorDialog(res: IRequestResult): Promise<void> {
    return new Promise((resolve) => {
        createModal([{type: "label", value: "An Error has occurred!"}], true, false).then(() => {
            resolve();
        });
    });
}
