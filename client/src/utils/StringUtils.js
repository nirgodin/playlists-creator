

export function titlize(lowercasedToken) {
    return lowercasedToken.charAt(0).toUpperCase() + lowercasedToken.slice(1);
}

export function toCamelCase(str) {
    let tokens = str.split(' ');
    let camelCasedTokens = [];

    for (const [index, token] of tokens.entries()) {
        const lowercasedToken = token.toLowerCase()
        
        if (index === 0) {
            camelCasedTokens.push(lowercasedToken)
        }
        else {
            let camelCasedToken = titlize(lowercasedToken);
            camelCasedTokens.push(camelCasedToken)
        }
    }

    return camelCasedTokens.join('')
}


export function getFirstLetter(str) {
    return str[0].toUpperCase();
}
