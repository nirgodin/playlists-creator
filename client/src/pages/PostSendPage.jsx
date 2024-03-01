import React, { useEffect, useState } from "react";
// import LoadingSpinner from "../components/LoadingSpinner";
import Confetti from "../components/Confetti";
import BackToMainPageButton from "../components/BackToMainPageButton";
import { Spotify } from "react-spotify-embed";
import PropTypes from "prop-types";
import { sendGetRequest } from "../utils/RequestsUtils";
import CircularProgressWithLabel from "../components/CircularProgressWithLabel";

function PostSendPage(props) {
  const stageProgressMapping = {
    ["playlist_details"]: 20,
    ["tracks"]: 50,
    ["cover"]: 90,
  };
  const [progress, setProgress] = useState(10);

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (!(props.isSuccessful)) {
        pollCaseProgress();
      } else {
        clearInterval(intervalId);
        handlePlaylistLink();
      }
    }, 3000);
  }, [props.isSuccessful]);

  async function pollCaseProgress() {
    const route = `cases/${props.caseId}/progress`;
    const caseStatus = await sendGetRequest(route, "caseStatus");
    const progress = stageProgressMapping[caseStatus];

    if (progress !== undefined) {
      setProgress(progress);
    }
    props.setIsSuccessful((caseStatus === "completed"));
  }

  async function handlePlaylistLink() {
    const route = `cases/${props.caseId}/playlist`;
    const playlistId = await sendGetRequest(route, "playlistId");
    const playlistLink = `https://open.spotify.com/playlist/${playlistId}`;
    props.setPlaylistLink(playlistLink);
  }

  if (!(props.isSuccessful && props.playlistLink !== "")) {
    return (
      <header className="spinner-container">
        <div>
          <p>Loading</p>
          <CircularProgressWithLabel value={progress} />
        </div>
      </header>
    );
  } else {
    return (
      <div className="sucess-page">
        <Confetti></Confetti>
        <h1>Congratulations! Your playlist was created</h1>
        <div className="playlist-iframe">
          <Spotify link={props.playlistLink} />
        </div>
        <div className="back-to-main-page-button">
          <BackToMainPageButton
            setWasRequestSent={props.setWasRequestSent}
            setIsSuccessful={props.setIsSuccessful}
          ></BackToMainPageButton>
        </div>
      </div>
    );
  }
}

PostSendPage.propTypes = {
  isSuccessful: PropTypes.bool,
  playlistLink: PropTypes.string,
  setPlaylistLink: PropTypes.func,
  setWasRequestSent: PropTypes.func,
  setIsSuccessful: PropTypes.func,
  caseId: PropTypes.string,
};

export default PostSendPage;
