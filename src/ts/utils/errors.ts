import {IRequestResult} from "../utils/request";
import {createModal} from "./modal";

export
function createErrorDialog(res: IRequestResult): Promise<void> {
    return new Promise((resolve) => {
        createModal([{type: "label", value: "An Error has occurred!"}], true, false).then(() => {
            resolve();
        });
    });
}
