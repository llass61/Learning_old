import 'whatwg-fetch';
// import { get } from 'https';

export function getUsers() {
    return get('users');
}

function get(url) {
    return fetch(url).then(onSuccess, onError);
}

function onSuccess(response) {
    return response.json();
}

function onError(error) {
    return console.log(error);
}
