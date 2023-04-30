import LoadingSpinner from "./LoadingSpinner";
import Confetti from "./Confetti";


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