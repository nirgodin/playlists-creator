import axios from "axios";

async function sendGetRequest(route, key) {
  const url = `${process.env.REACT_APP_BASE_URL}/${route}`;
  return await axios
    .get(url, {
      auth: {
        username: process.env.REACT_APP_USERNAME,
        password: process.env.REACT_APP_PASSWORD,
      },
    })
    .then((resp) => JSON.stringify(resp.data))
    .then((data) => JSON.parse(data))
    .then((jsonfiedData) => jsonfiedData[key]);
}

export { sendGetRequest };
