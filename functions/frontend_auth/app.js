import cf from 'cloudfront';
const kvsHandle = cf.kvs();

async function handler(event) {
    let authUser = "tmp";
    let authPass = "tmp";
    try {
        authUser = await kvsHandle.get("username", { format: "string"});
        authPass = await kvsHandle.get("password", { format: "string"});
    } catch (err) {
        console.log(`Kvs key lookup failed`);
    }

    var request = event.request;
    var headers = request.headers;

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