import axios from 'axios';

async function getDefaultRequestBody() {
    const url = `${process.env.REACT_APP_BASE_URL}/requestBody`;
    return await axios.get(url)
      .then((resp) => JSON.stringify(resp.data))
      .then((data) => JSON.parse(data))
      .then((jsonfiedData) => jsonfiedData['requestBody'])
  };

export {getDefaultRequestBody}