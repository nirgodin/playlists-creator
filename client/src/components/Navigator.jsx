import { useState } from "react";
import RequestBody from "./RequestBody";
import SendButton from "./SendButton";
import LoadingSpinner from "./LoadingSpinner";
import Confetti from "./Confetti";
import MethodToggleButton from "./MethodToggleButton";
import FormTextField from "./FormTextField";
import { Box } from "@mui/material";

export default function Navigator(props) {
    const [wasRequestSent, setWasRequestSent] = useState(false)
    const [isSuccessfull, setIsSuccessfull] = useState(false)
    const [alignment, setAlignment] = useState('prompt');
    const endpoint = alignment === 'prompt' ? 'fromPrompt' : 'fromParams'
    const sendButton = <Box>
        <SendButton
            text={'Create Playlist'}
            endpoint={endpoint}
            body={props.body[0]}
            setWasRequestSent={setWasRequestSent}
            setIsSuccessfull={setIsSuccessfull}
        ></SendButton>
    </Box>

    if (!wasRequestSent) {
        if (alignment === 'prompt') {
            return (
                <div>
                    <Box>
                        <div className="toggle-button">
                            <MethodToggleButton
                                alignment={alignment}
                                setAlignment={setAlignment}
                            ></MethodToggleButton>
                        </div>
                        <div className="text-field">
                            <FormTextField
                                isRequired={true}
                                id={'prompt'}
                                label={"Prompt"}
                                defaultValue={''}
                                body={props.body}
                                setBody={props.setBody}
                            ></FormTextField>
                        </div>
                        {sendButton}
                    </Box>
                </div>
            )
        }
        else {
            return (
                <div>
                    <MethodToggleButton
                        alignment={alignment}
                        setAlignment={setAlignment}
                    ></MethodToggleButton>
                    <RequestBody body={props.body} setBody={props.setBody}></RequestBody>
                    {sendButton}
                </div>
            )
        }

    } else {
        if (!isSuccessfull) {
            return <LoadingSpinner></LoadingSpinner>
        }
        else {
            return <div>
                <Confetti></Confetti>
                <h1>Congratulations! Your playlist was created</h1>
            </div>
        }
    }
    // {<p>{JSON.stringify(body[0])}</p>}
}