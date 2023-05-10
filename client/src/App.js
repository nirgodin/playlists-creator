import './App.css';
import React, { useEffect } from 'react';
import Navigator from './Navigator'
import { useState } from 'react';
import _ from 'underscore';
import LoadingSpinner from './components/LoadingSpinner';
import { getDefaultRequestBody } from './utils/RequestsUtils'

function App() {
  const [body, setBody] = useState([]);
  const [defaultRequestBody, setDefaultRequestBody] = useState([]);

  async function setRequestBody() {
    const requestBody = await getDefaultRequestBody();
    const clonedRequestBody = JSON.parse(JSON.stringify(requestBody));
    setDefaultRequestBody(clonedRequestBody);
    const secondClonedRequestBody = JSON.parse(JSON.stringify(requestBody));
    setBody(Array.from(secondClonedRequestBody));
  };

  useEffect(
    () => {
      if (_.isEqual(body, []) || _.isEqual(defaultRequestBody, [])) {
        setRequestBody()
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
            defaultRequestBody={defaultRequestBody}
          ></Navigator>
        </header>
      </div>
    );
  }
}

export default App;
