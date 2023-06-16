export function toTitle(lowercasedToken) {
  return lowercasedToken.charAt(0).toUpperCase() + lowercasedToken.slice(1);
}

export function toCamelCase(str) {
  let tokens = str.split(" ");
  let camelCasedTokens = [];

  for (const [index, token] of tokens.entries()) {
    const lowercasedToken = token.toLowerCase();

    if (index === 0) {
      camelCasedTokens.push(lowercasedToken);
    } else {
      let camelCasedToken = toTitle(lowercasedToken);
      camelCasedTokens.push(camelCasedToken);
    }
  }

  return camelCasedTokens.join("");
}

export function convertCamelToTitle(camelCaseString) {
  var words = camelCaseString.split(/(?=[A-Z])/);
  var titleCaseString = words.map(function(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
  }).join(' ');

  return titleCaseString;
}