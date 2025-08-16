function handler(event) {
    var request = event.request;
    var headers = request.headers;

    // This is populated by the script that inlines this code into the SAM template
    var authUser = '__CLOUDFRONT_USERNAME__';
    var authPass = '__CLOUDFRONT_PASSWORD__';

    var authString = 'Basic ' + btoa(authUser + ':' + authPass);

    var authHeader = headers['authorization'];

    if (!authHeader || authHeader.value !== authString) {
        return {
            statusCode: 401,
            statusDescription: 'Unauthorized',
            headers: {
                'www-authenticate': {
                    value: 'Basic'
                }
            },
            body: 'Unauthorized'
        };
    }

    return request;
}