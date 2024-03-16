import React, { useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";
import { sendGetRequest } from "../utils/RequestsUtils";
import CircularProgressWithLabel from "../components/CircularProgressWithLabel";
import { STAGE_PROGRESS_MAPPING, STAGE_TEXT_MAPPING } from "../consts";

function PostSendPage({
  isSuccessful,
  setIsSuccessful,
  setPlaylistLink,
  caseId,
}) {
  let intervalNumber = useRef(1);
  const [progress, setProgress] = useState(0);
  const [text, setText] = useState("Request received!");

  useEffect(() => {
    async function pollCaseProgress() {
      const route = `cases/${caseId}/progress`;
      const caseStatus = await sendGetRequest(route, "caseStatus");
      const currentProgress = STAGE_PROGRESS_MAPPING[caseStatus];

      if (currentProgress !== undefined) {
        setProgress(currentProgress);
        setText(STAGE_TEXT_MAPPING[caseStatus]);
      }
      setIsSuccessful(caseStatus === "completed");
    }

    async function handlePlaylistLink() {
      const route = `cases/${caseId}/playlist`;
      const playlistId = await sendGetRequest(route, "playlistId");
      const playlistLink = `https://open.spotify.com/playlist/${playlistId}`;
      setPlaylistLink(playlistLink);
    }

    const intervalId = setInterval(() => {
      if (intervalNumber.current % 3 === 0) {
        pollCaseProgress();
      } else {
        setProgress((previousProgress) =>
          previousProgress <= 98 ? previousProgress + 1 : previousProgress
        );
      }

      if (isSuccessful) {
        handlePlaylistLink();
      }
      intervalNumber.current = intervalNumber.current + 1;
    }, 1000);

    return () => {clearInterval(intervalId)}
  }, [isSuccessful, caseId, setPlaylistLink, setIsSuccessful, setProgress]);

  return (
    <header className="spinner-container">
      <div>
        <p>{text}</p>
        <CircularProgressWithLabel value={progress} />
      </div>
    </header>
  );
}

PostSendPage.propTypes = {
  isSuccessful: PropTypes.bool,
  setPlaylistLink: PropTypes.func,
  setIsSuccessful: PropTypes.func,
  caseId: PropTypes.string,
};

export default PostSendPage;
