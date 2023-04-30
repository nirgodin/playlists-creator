import { useState } from "react";
import LandingPage from "./LandingPage";
import PostSendPage from "./PostSendPage";

export default function Navigator(props) {
    const [wasRequestSent, setWasRequestSent] = useState(false)
    const [isSuccessfull, setIsSuccessfull] = useState(false)

    if (!wasRequestSent) {
        return (
            <div>
            <LandingPage
                body={props.body}
                setBody={props.setBody}
                setWasRequestSent={setWasRequestSent}
                setIsSuccessfull={setIsSuccessfull}
            ></LandingPage>
            {/* <p>{JSON.stringify(props.body[0])}</p> */}
            </div>
        )

    } else {
        return (
            <PostSendPage
                isSuccessfull={isSuccessfull}
            ></PostSendPage>
        )
    }
}