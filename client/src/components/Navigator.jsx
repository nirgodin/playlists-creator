import { useState, useEffect } from "react";
import LandingPage from "./LandingPage";
import PostSendPage from "./PostSendPage";
import { isLoggedIn, extractCode } from "../utils/UrlUtils";
import LoginPage from "./LoginPage";
import ErrorPage from "./ErrorPage";

export default function Navigator(props) {
    const [wasRequestSent, setWasRequestSent] = useState(false)
    const [isSuccessfull, setIsSuccessfull] = useState(false)
    const [isError, setIsError] = useState(false)

    useEffect(
        () => {
            if (isLoggedIn()) {
                let newBody = props.body[0]
                newBody['accessCode'] = extractCode(window.location.href);
                props.setBody([newBody]);
            }
        }, [props]
    )

    if (!isLoggedIn()) {
        return <LoginPage
            body={props.body}
            setBody={props.setBody}
        ></LoginPage>
    } else if (!wasRequestSent) {
        return (
            <div>
                <LandingPage
                    body={props.body}
                    setBody={props.setBody}
                    setWasRequestSent={setWasRequestSent}
                    setIsSuccessfull={setIsSuccessfull}
                    setIsError={setIsError}
                ></LandingPage>
                {/* <p>{JSON.stringify(props.body[0])}</p> */}
            </div>
        )
    } else if (isError) {
        return (
            <ErrorPage></ErrorPage>
        )
    } else {
        return (
            <PostSendPage
                isSuccessfull={isSuccessfull}
            ></PostSendPage>
        )
    }
}