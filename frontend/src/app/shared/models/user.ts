export class User {
    id: string;
    integrations: IntegrationType[]

    constructor(data: {id: string, integrations: string[]}) {
        const validValues = Object.values(IntegrationType);
        const invalid = data.integrations.filter(i => !validValues.includes(i as IntegrationType));
        if (invalid.length > 0) {
            throw new Error(
                `Invalid integration type(s): "${invalid.join(', ')}". ` +
                `Allowed types are: ${validValues.join(', ')}`
            );
        }
        this.id = data.id;
        this.integrations = data.integrations.map(i => i as IntegrationType);
    }

}

export enum IntegrationType {
    SPOTIFY = "spotify",
    TIDAL = "tidal",
}