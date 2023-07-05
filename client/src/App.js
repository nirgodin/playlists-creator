import "./App.css";
import React, { useCallback, useEffect } from "react";
import Navigator from "./Navigator";
import { useState } from "react";
import _ from "underscore";
import LoadingSpinner from "./components/LoadingSpinner";
import { sendGetRequest } from "./utils/RequestsUtils";
import cloneJSON from "./utils/JsonUtils";
import { CREATE_PLAYLIST, REQUEST_BODY } from "./consts";
import ResponsiveAppBar from "./components/ResponsiveAppBar";

function App() {
  const [body, setBody] = useState([]);
  const [defaultRequestBody, setDefaultRequestBody] = useState([]);
  const [currentPage, setCurrentPage] = useState(CREATE_PLAYLIST);

  async function setRequestBody() {
    const requestBody = await sendGetRequest(REQUEST_BODY, REQUEST_BODY);
    setDefaultRequestBody(cloneJSON(requestBody));
    setBody(requestBody);
  }

  const memoizedEffect = useCallback(() => {
    if (_.isEqual(body, []) || _.isEqual(defaultRequestBody, [])) {
      setRequestBody();
    }
  }, [body, defaultRequestBody]);

  useEffect(memoizedEffect, []);

  if (_.isEqual(body, [])) {
    return (
      <div className="App">
        <header className="App-header">
          <LoadingSpinner></LoadingSpinner>
        </header>
      </div>
    );
  } else if (currentPage === CREATE_PLAYLIST) {
    return (
      <div className="App">
        <ResponsiveAppBar
          currentPage={currentPage}
          setCurrentPage={setCurrentPage}
        ></ResponsiveAppBar>
        <header className="App-header">
          <Navigator
            body={body}
            setBody={setBody}
            defaultRequestBody={defaultRequestBody}
          ></Navigator>
        </header>
      </div>
    );
  } else {
    return (
      <div className="App">
        <ResponsiveAppBar
          currentPage={currentPage}
          setCurrentPage={setCurrentPage}
        ></ResponsiveAppBar>
        <header className="App-header">
          <h1>Featured Playlists!</h1>
        </header>
      </div>
    );
  }
}

export default App;
