export enum IntegrationType {
    SPOTIFY = "SPOTIFY",
    TIDAL = "TIDAL",
}

export class Integration {
    id: string;
    type: IntegrationType;

    constructor(data: {id: string, type: string}) {
        if (!(Object.values(IntegrationType) as string[]).includes(data.type)) {
            throw new Error(
                `Invalid integration type: "${data.type}". `
            );
        }
        this.id = data.id;
        this.type = data.type as IntegrationType;
    }

}