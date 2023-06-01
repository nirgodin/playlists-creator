import React from "react";
import LoadingSpinner from "../components/LoadingSpinner";
import Confetti from "../components/Confetti";
import BackToMainPageButton from "../components/BackToMainPageButton";
import { Spotify } from "react-spotify-embed";
import PropTypes from 'prop-types';

function PostSendPage(props) {
    if (!props.isSuccessful) {
        return <LoadingSpinner></LoadingSpinner>
    }
    else {
        return <div className="sucess-page">
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
    }
}

PostSendPage.propTypes = {
    isSuccessful: PropTypes.bool,
    playlistLink: PropTypes.string,
    setWasRequestSent: PropTypes.func,
    setIsSuccessful: PropTypes.func
}

export default PostSendPage;