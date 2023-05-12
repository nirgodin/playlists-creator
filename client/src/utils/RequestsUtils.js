import axios from 'axios';
import { REQUEST_BODY } from '../consts';

async function getDefaultRequestBody() {
    const url = `${process.env.REACT_APP_BASE_URL}/${REQUEST_BODY}`;
    return await axios.get(url)
      .then((resp) => JSON.stringify(resp.data))
      .then((data) => JSON.parse(data))
      .then((jsonfiedData) => jsonfiedData[REQUEST_BODY])
  };

export {getDefaultRequestBody}