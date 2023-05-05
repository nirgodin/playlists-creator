import './App.css';
import React, { useEffect } from 'react';
import Navigator from './Navigator'
import { useState } from 'react';
import axios from 'axios'
import _ from 'underscore'
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [body, setBody] = useState([])

  const getDefaultRequestBody = async () => {
    const url = `${process.env.REACT_APP_BASE_URL}/requestBody`;
    await axios.get(url)
      .then((resp) => JSON.stringify(resp.data))
      .then((data) => JSON.parse(data))
      .then((jsonfiedData) => jsonfiedData['requestBody'])
      .then((requestBody) => setBody(requestBody))
  };

  useEffect(
    () => {
      if (_.isEqual(body, [])) {
        getDefaultRequestBody()
      }
    }
  )

  if (_.isEqual(body, [])) {
    return (
      <div className="App">
        <header className="App-header">
          <LoadingSpinner></LoadingSpinner>
        </header>
      </div>
    );
  } else {
    return (
      <div className="App">
        <header className="App-header">
          <Navigator
            body={body}
            setBody={setBody}
          ></Navigator>
        </header>
      </div>
    );
  }
}

export default App;
