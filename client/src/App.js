import "./App.css";
import React, { useCallback, useEffect } from "react";
import { useState } from "react";
import _ from "underscore";
import { sendGetRequest } from "./utils/RequestsUtils";
import cloneJSON from "./utils/JsonUtils";
import { CREATE_PLAYLIST, REQUEST_BODY } from "./consts";
import ResponsiveAppBar from "./components/ResponsiveAppBar";
import AppNavigator from "./navigators/AppNavigator";
import { isLoggedIn } from "./utils/UrlUtils";

function App() {
  const [body, setBody] = useState([]);
  const [defaultRequestBody, setDefaultRequestBody] = useState([]);
  const [currentPage, setCurrentPage] = useState(CREATE_PLAYLIST);
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(isLoggedIn());

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

  return (
    <div className="App">
      <ResponsiveAppBar
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        isUserLoggedIn={isUserLoggedIn}
        setIsUserLoggedIn={setIsUserLoggedIn}
      ></ResponsiveAppBar>
      <header className="App-header">
        <AppNavigator
          body={body}
          setBody={setBody}
          defaultRequestBody={defaultRequestBody}
          currentPage={currentPage}
          isUserLoggedIn={isUserLoggedIn}
        ></AppNavigator>
      </header>
    </div>
  );
}

export default App;
