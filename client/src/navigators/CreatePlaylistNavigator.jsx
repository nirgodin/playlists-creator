import React from "react";
import { useState, useEffect } from "react";
import LandingPage from "../pages/LandingPage";
import PostSendPage from "../pages/PostSendPage";
import { extractCode } from "../utils/UrlUtils";
import LoginPage from "../pages/LoginPage";
import LoadingSpinner from "../components/LoadingSpinner";
import { ACCESS_CODE } from "../consts";
import PropTypes from "prop-types";

function CreatePlaylistNavigator(props) {
  const [wasRequestSent, setWasRequestSent] = useState(false);
  const [isSuccessful, setIsSuccessful] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [playlistLink, setPlaylistLink] = useState("");
  const [caseId, setCaseId] = useState(undefined);

  useEffect(() => {
    if (props.isUserLoggedIn && props.body[0][ACCESS_CODE] === "") {
      let newBody = props.body[0];
      const extractedAccessCode = extractCode(window.location.href);
      newBody[ACCESS_CODE] = extractedAccessCode;
      props.setBody([newBody]);
    }
  }, [props]);

  if (!props.isUserLoggedIn) {
    return (
      <div>
        <LoginPage
          body={props.body}
          setBody={props.setBody}
          errorMessage={errorMessage}
        ></LoginPage>
      </div>
    );
  } else if (!wasRequestSent || errorMessage !== "") {
    return (
      <div>
        <LandingPage
          body={props.body}
          setBody={props.setBody}
          defaultRequestBody={props.defaultRequestBody}
          setWasRequestSent={setWasRequestSent}
          setIsSuccessful={setIsSuccessful}
          errorMessage={errorMessage}
          setErrorMessage={setErrorMessage}
          setPlaylistLink={setPlaylistLink}
          setCaseId={setCaseId}
        ></LandingPage>
      </div>
    );
  } else if (caseId !== undefined) {
    return (
      <PostSendPage
        isSuccessful={isSuccessful}
        setWasRequestSent={setWasRequestSent}
        setIsSuccessful={setIsSuccessful}
        setPlaylistLink={setPlaylistLink}
        playlistLink={playlistLink}
        caseId={caseId}
      ></PostSendPage>
    );
  } else {
    return <LoadingSpinner></LoadingSpinner>;
  }
}

CreatePlaylistNavigator.propTypes = {
  body: PropTypes.array,
  defaultRequestBody: PropTypes.array,
  setBody: PropTypes.func,
  isUserLoggedIn: PropTypes.bool,
};

export default CreatePlaylistNavigator;
