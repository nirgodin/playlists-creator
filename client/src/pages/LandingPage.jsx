import MethodToggleButton from ".././components/MethodToggleButton"
import { Box } from "@mui/material"
import FormTextField from ".././components/FormTextField"
import SendButton from ".././components/SendButton"
import { useState, useEffect } from "react"
import RequestBody from ".././components/RequestBody"
import PlaylistTextFields from ".././components/PlaylistTextFields"
import { PROMPT, CONFIGURATION } from "../consts"

export default function LandingPage(props) {
    const [alignment, setAlignment] = useState(PROMPT);
    const endpoint = alignment === PROMPT ? PROMPT : CONFIGURATION
    const [isValidInput, setIsValidInput] = useState(false)
    const [isValidPrompt, setIsValidPrompt] = useState(false)
    const [isValidPlaylistName, setIsValidPlaylistName] = useState(false)

    useEffect(
        () => {
            if (endpoint === PROMPT) {
                const isValid = (isValidPrompt && isValidPlaylistName);
                setIsValidInput(isValid);
            } else {
                setIsValidInput(isValidPlaylistName);
            }
        }, [endpoint, isValidPrompt, isValidPlaylistName]
    )

    const playlistDetails = <div className='playlist-details'>
        <PlaylistTextFields
            body={props.body}
            setBody={props.setBody}
            isValidPlaylistName={isValidPlaylistName}
            setIsValidPlaylistName={setIsValidPlaylistName}
        ></PlaylistTextFields>
    </div>

    const toggleButton = <div className="toggle-button">
        <MethodToggleButton
            alignment={alignment}
            setAlignment={setAlignment}
        ></MethodToggleButton>
    </div>

    const buttons = <div>
        <Box>
            <SendButton
                text={'Create Playlist'}
                endpoint={endpoint}
                body={props.body}
                setBody={props.setBody}
                defaultRequestBody={props.defaultRequestBody}
                setWasRequestSent={props.setWasRequestSent}
                setIsSuccessfull={props.setIsSuccessfull}
                setErrorMessage={props.setErrorMessage}
                setPlaylistLink={props.setPlaylistLink}
                isValidInput={isValidInput}
            ></SendButton>
        </Box>
        <p className="skew-y-shaking" key={props.errorMessage}>{props.errorMessage}</p>
    </div>

    if (alignment === PROMPT) {
        return (
            <div>
                {playlistDetails}
                <Box>
                    {toggleButton}
                    <div className="text-field">
                        <FormTextField
                            isRequired={true}
                            id={PROMPT}
                            label={"Prompt"}
                            defaultValue={''}
                            body={props.body}
                            setBody={props.setBody}
                            isValidInput={isValidPrompt}
                            setIsValidInput={setIsValidPrompt}
                        ></FormTextField>
                    </div>
                    {buttons}
                </Box>
            </div>
        )
    }
    else {
        return (
            <div>
                {playlistDetails}
                {toggleButton}
                <RequestBody
                    body={props.body}
                    setBody={props.setBody}
                ></RequestBody>
                {buttons}
            </div>
        )
    }
}