import { useState } from "react";
import RequestBody from "./RequestBody";
import SendButton from "./SendButton";
import LoadingSpinner from "./LoadingSpinner";
import Confetti from "./Confetti";

export default function Navigator() {
    const [wasRequestSent, setWasRequestSent] = useState(false)
    const [isSuccessfull, setIsSuccessfull] = useState(false)
    const [body, setBody] = useState(
        [
            {
                'filterParams': {
                    'mainGenre': {
                        'operator': 'in',
                        'value': []
                    },
                    'language': {
                        'operator': 'in',
                        'value': []
                    },
                    'minPopularity': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxPopularity': {
                        'operator': '<',
                        'value': 100
                    },
                    'minDanceability': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxDanceability': {
                        'operator': '<',
                        'value': 100
                    },
                    'minEnergy': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxEnergy': {
                        'operator': '<',
                        'value': 100
                    },
                    'minLoudness': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxLoudness': {
                        'operator': '<',
                        'value': 100
                    },
                    'minMode': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxMode': {
                        'operator': '<',
                        'value': 100
                    },
                    'minSpeechiness': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxSpeechiness': {
                        'operator': '<',
                        'value': 100
                    },
                    'minAcousticness': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxAcousticness': {
                        'operator': '<',
                        'value': 100
                    },
                    'minInstrumentalness': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxInstrumentalness': {
                        'operator': '<',
                        'value': 100
                    },
                    'minLiveness': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxLiveness': {
                        'operator': '<',
                        'value': 100
                    },
                    'minValence': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxValence': {
                        'operator': '<',
                        'value': 100
                    },
                    'minTempo': {
                        'operator': '>',
                        'value': 0
                    },
                    'maxTempo': {
                        'operator': '<',
                        'value': 100
                    }
                },
                'accessCode': '',
                'playlistDetails': {
                    'playlistName': '',
                    'playlistDescription': '',
                    'isPublic': false
                }
            }
        ]
    )

    if (!wasRequestSent) {
        return (
            <div>
                <RequestBody body={body} setBody={setBody}></RequestBody>
                <SendButton
                    text={'Create Playlist'}
                    url='http://127.0.0.1:5000/fromParams'
                    body={body[0]}
                    setWasRequestSent={setWasRequestSent}
                    setIsSuccessfull={setIsSuccessfull}
                ></SendButton>
            </div>
        )
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
    // {<p>{JSON.stringify(props.body[0])}</p>}
}