import React, { useCallback, useEffect, useRef, useState } from "react";
// import LoadingSpinner from "../components/LoadingSpinner";
import Confetti from "../components/Confetti";
import BackToMainPageButton from "../components/BackToMainPageButton";
import { Spotify } from "react-spotify-embed";
import PropTypes from "prop-types";
import { sendGetRequest } from "../utils/RequestsUtils";
import CircularProgressWithLabel from "../components/CircularProgressWithLabel";

const STAGE_PROGRESS_MAPPING = {
  ["playlist_details"]: 40,
  ["tracks"]: 70,
  ["cover"]: 90,
};

const STAGE_TEXT_MAPPING = {
  ["playlist_details"]: "Selecting tracks",
  ["tracks"]: "Creating playlist cover",
  ["cover"]: "Almost there!",
};

function PostSendPage(props) {
  let intervalNumber = useRef(1);
  const [progress, setProgress] = useState(10);
  const [text, setText] = useState("Request received!")

  const pollCaseProgress = useCallback(async () => {
    const route = `cases/${props.caseId}/progress`;
    const caseStatus = await sendGetRequest(route, "caseStatus");
    const currentProgress = STAGE_PROGRESS_MAPPING[caseStatus];

    if (currentProgress !== undefined) {
      if (currentProgress > progress) {
        setProgress(currentProgress);
      }

      setText(STAGE_TEXT_MAPPING[caseStatus]);
    }
    props.setIsSuccessful((caseStatus === "completed"));
  }, [props])

  const handlePlaylistLink = useCallback(async () => {
    const route = `cases/${props.caseId}/playlist`;
    const playlistId = await sendGetRequest(route, "playlistId");
    const playlistLink = `https://open.spotify.com/playlist/${playlistId}`;
    props.setPlaylistLink(playlistLink);
  }, [props])

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (props.isSuccessful) {
        clearInterval(intervalId);
        handlePlaylistLink();
      } else if (intervalNumber.current % 3 === 0) {
        pollCaseProgress();
      } else {
        setProgress((previousProgress) => previousProgress + 1);
      }

      intervalNumber.current = intervalNumber.current + 1;
    }, 1000);
  }, [props.isSuccessful, handlePlaylistLink, pollCaseProgress]);

  if (!(props.isSuccessful && props.playlistLink !== "")) {
    return (
      <header className="spinner-container">
        <div>
          <p>{text}</p>
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
