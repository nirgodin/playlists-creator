
const SPOTIFY_BASE_AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize?'

function generateAccessCodeURL(clientID, redirectURI) {
    console.log(`Redirect URI ${redirectURI}`);
    const params = {
        client_id: clientID,
        response_type: 'code',
        redirect_uri: redirectURI,
        scope: 'playlist-modify-public playlist-modify-private user-read-private',
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