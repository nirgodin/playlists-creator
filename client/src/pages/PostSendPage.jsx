import LoadingSpinner from "../components/LoadingSpinner";
import Confetti from "../components/Confetti";


export default function PostSendPage(props) {
    if (!props.isSuccessfull) {
        return <LoadingSpinner></LoadingSpinner>
    }
    else {
        return <div>
            <Confetti></Confetti>
            <h1>Congratulations! Your playlist was created</h1>
        </div>
    }
}