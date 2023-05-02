import MethodToggleButton from ".././components/MethodToggleButton"
import { Box } from "@mui/material"
import FormTextField from ".././components/FormTextField"
import SendButton from ".././components/SendButton"
import { useState } from "react"
import RequestBody from ".././components/RequestBody"
import PlaylistTextFields from ".././components/PlaylistTextFields"

export default function LandingPage(props) {
    const [alignment, setAlignment] = useState('prompt');
    const endpoint = alignment === 'prompt' ? 'fromPrompt' : 'fromParams'

    const playlistDetails = <div className='playlist-details'>
        <PlaylistTextFields
            body={props.body}
            setBody={props.setBody}
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
                body={props.body[0]}
                setWasRequestSent={props.setWasRequestSent}
                setIsSuccessfull={props.setIsSuccessfull}
                setIsError={props.setIsError}
            ></SendButton>
        </Box>
    </div>

    if (alignment === 'prompt') {
        return (
            <div>
                {playlistDetails}
                <Box>
                    {toggleButton}
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