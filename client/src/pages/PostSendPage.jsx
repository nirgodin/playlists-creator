import LoadingSpinner from "../components/LoadingSpinner";
import Confetti from "../components/Confetti";
import BackToMainPageButton from "../components/BackToMainPageButton";


export default function PostSendPage(props) {
    if (!props.isSuccessfull) {
        return <LoadingSpinner></LoadingSpinner>
    }
    else {
        return <div>
            <Confetti></Confetti>
            <h1>Congratulations! Your playlist was created</h1>
            <h2>Search your spotify playlists section to find it using the name you selected</h2>
            <BackToMainPageButton
                setWasRequestSent={props.setWasRequestSent}
            ></BackToMainPageButton>
        </div>
    }
}