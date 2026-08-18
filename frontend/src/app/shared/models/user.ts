export class User {
    id: string;
    integrations: IntegrationType[]

    constructor(data: {id: string, integrations: string[]}) {
        const validValues = Object.values(IntegrationType);
        if (data.integrations != undefined) {
            const invalid = data.integrations.filter(i => !validValues.includes(i as IntegrationType));
            if (invalid.length > 0) {
                throw new Error(
                    `Invalid integration type(s): "${invalid.join(', ')}". ` +
                    `Allowed types are: ${validValues.join(', ')}`
                );
            }
            this.integrations = data.integrations.map(i => i as IntegrationType);
        } else {
            this.integrations = [];
        }
        this.id = data.id;
    }

}

export enum IntegrationType {
    SPOTIFY = "spotify",
    TIDAL = "tidal",
}