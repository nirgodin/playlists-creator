import LoadingSpinner from "../components/LoadingSpinner";
import Confetti from "../components/Confetti";
import BackToMainPageButton from "../components/BackToMainPageButton";
import { Spotify } from "react-spotify-embed";


export default function PostSendPage(props) {
    if (!props.isSuccessfull) {
        return <LoadingSpinner></LoadingSpinner>
    }
    else {
        return <div>
            <Confetti></Confetti>
            <h1>Congratulations! Your playlist was created</h1>
            <div className="playlist-iframe">
                <Spotify link={props.playlistLink} />
            </div>
            <div className="back-to-main-page-button">
                <BackToMainPageButton
                    setWasRequestSent={props.setWasRequestSent}
                    setIsSuccessfull={props.setIsSuccessfull}
                ></BackToMainPageButton>
            </div>
        </div>
    }
}