import React from "react";
import { useState, useEffect } from "react";
import LandingPage from "../pages/LandingPage";
import PostSendPage from "../pages/PostSendPage";
import { extractCode } from "../utils/UrlUtils";
import LoginPage from "../pages/LoginPage";
import LoadingSpinner from "../components/LoadingSpinner";
import { ACCESS_CODE } from "../consts";
import PropTypes from "prop-types";
import PlaylistPage from "../pages/PlaylistPage";

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
      <div key={"login-page"}>
        <LoginPage
          body={props.body}
          setBody={props.setBody}
          errorMessage={errorMessage}
        ></LoginPage>
      </div>
    );
  } else if (!wasRequestSent || errorMessage !== "") {
    return (
      <div key={"landing-page"}>
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
  } else if (!(isSuccessful && playlistLink !== "")) {
    return (
      <PostSendPage
        key={"post-send-page"}
        isSuccessful={isSuccessful}
        setIsSuccessful={setIsSuccessful}
        setPlaylistLink={setPlaylistLink}
        caseId={caseId}
      ></PostSendPage>
    );
  } else if (isSuccessful) {
    return (
      <PlaylistPage
        key={"playlist-page"}
        playlistLink={playlistLink}
        setWasRequestSent={setWasRequestSent}
        setIsSuccessful={setIsSuccessful}
      ></PlaylistPage>
    )
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
