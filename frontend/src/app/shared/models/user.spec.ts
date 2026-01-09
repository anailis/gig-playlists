import { User } from './user';

describe('User', () => {
    it('should create an user with a valid integration type', () => {
        const data = { id: '123', integrations: ['spotify'] };
        const user = new User(data);

        expect(user.id).toBe('123');
        expect(user.integrations[0]).toBe('spotify');
    });

    it('should throw an error when invalid integration supplied', () => {
        const data = { id: '123', integrations: ['spotify', 'invalid'] };

        expect(() => new User(data)).toThrowError(
            /Invalid integration type\(s\): "invalid"/
        );
    });

    it('should show allowed integration types in error message', () => {
        const data = { id: '456', integrations: ['invalid'] };

        expect(() => new User(data)).toThrowError(
            /Allowed types are: spotify, tidal/
        );
    });
});