
const SPOTIFY_BASE_AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize?'
const SPOTIFY_SCOPES = [
    'playlist-modify-public',
    'playlist-modify-private',
    'user-read-private',
    'ugc-image-upload'
]

function generateAccessCodeURL(clientID, redirectURI) {
    console.log(`Redirect URI ${redirectURI}`);
    const params = {
        client_id: clientID,
        response_type: 'code',
        redirect_uri: redirectURI,
        scope: SPOTIFY_SCOPES.join(' ')
    };
    return SPOTIFY_BASE_AUTHORIZATION_URL + Object.entries(params).map(kv => kv.map(encodeURIComponent).join("=")).join("&");
}

function isLoggedIn() {
    return window.location.href.includes('?code=')
}

function extractCode(href) {
    return href.split('code=')[1];
}

export {generateAccessCodeURL, isLoggedIn, extractCode}
