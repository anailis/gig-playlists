import {Integration} from "@models/integration";

export class User {
    id: string;
    integrations: Integration[]

    constructor(data: {id: string, integrations: Integration[]}) {
        if (data.integrations != undefined) {
            this.integrations = data.integrations;
        } else {
            this.integrations = [];
        }
        this.id = data.id;
    }

}