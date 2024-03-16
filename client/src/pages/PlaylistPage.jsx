import React from "react";
import Confetti from "../components/Confetti";
import BackToMainPageButton from "../components/BackToMainPageButton";
import { Spotify } from "react-spotify-embed";
import PropTypes from "prop-types";

function PlaylistPage({playlistLink, setWasRequestSent, setIsSuccessful}) {
  return (
    <div className="success-page">
      <Confetti></Confetti>
      <h1>Congratulations! Your playlist was created</h1>
      <div className="playlist-iframe">
        <Spotify link={playlistLink} />
      </div>
      <div className="back-to-main-page-button">
        <BackToMainPageButton
          setWasRequestSent={setWasRequestSent}
          setIsSuccessful={setIsSuccessful}
        ></BackToMainPageButton>
      </div>
    </div>
  );
}

PlaylistPage.propTypes = {
  playlistLink: PropTypes.string,
  setWasRequestSent: PropTypes.func,
  setIsSuccessful: PropTypes.func,
};

export default PlaylistPage;
