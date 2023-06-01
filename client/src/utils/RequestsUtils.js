import axios from 'axios';

async function sendGetRequest(route, key) {
    const url = `${process.env.REACT_APP_BASE_URL}/${route}`;
    return await axios.get(url)
      .then((resp) => JSON.stringify(resp.data))
      .then((data) => JSON.parse(data))
      .then((jsonfiedData) => jsonfiedData[key])
  }

export {sendGetRequest}