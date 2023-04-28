
const SPOTIFY_BASE_AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize?'

export default function generateAccessCodeURL(clientID, redirectURI) {
    const params = {
        client_id: clientID,
        response_type: 'code',
        redirect_uri: redirectURI,
        scope: 'playlist-modify-public playlist-modify-private'
    };
    return SPOTIFY_BASE_AUTHORIZATION_URL + Object.entries(params).map(kv => kv.map(encodeURIComponent).join("=")).join("&");
}