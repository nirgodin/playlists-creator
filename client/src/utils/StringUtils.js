

export default function toCamelCase(str) {
    let tokens = str.split(' ');
    let camelCasedTokens = [];

    for (const [index, token] of tokens.entries()) {
        const lowercasedToken = token.toLowerCase()
        
        if (index === 0) {
            camelCasedTokens.push(lowercasedToken)
        }
        else {
            let camelCasedToken = lowercasedToken.charAt(0).toUpperCase() + lowercasedToken.slice(1);
            camelCasedTokens.push(camelCasedToken)
        }
    }

    return camelCasedTokens.join('')
}