import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import MultipleSelectChip from './MultipleSelectChip';
import { languageLabels, genreLabels } from '../consts';
import { useState } from 'react';
import SendButton from './SendButton';
import './RequestBody.css'
import MultipleSelectChipWrapper from './MultipleSelectChipWrapper';
import LoginButton from './LoginButton';
import PlaylistTextFields from './PlaylistTextFields';
import AudioFeaturesSliders from './AudioFeaturesSliders';
import Section from './Section';
import LoadingSpinner from './LoadingSpinner';

export default function RequestBody(props) {
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
    return <div>
        <div className='playlist-details'>
            <PlaylistTextFields
                body={props.body[0]}
                setBody={props.setBody}
            ></PlaylistTextFields>
        </div>
        <div className='playlist-configuration'>
            <Section
                header='Audio Features'
                sectionDetails={
                    <AudioFeaturesSliders
                        body={props.body}
                        setBody={props.setBody}
                    ></AudioFeaturesSliders>
                }
            ></Section>
            <MinDistanceRangeSlider
                minDistance={10}
                title={'Popularity'}
                body={props.body}
                setBody={props.setBody}
            ></MinDistanceRangeSlider>
            <MultipleSelectChipWrapper
                title={'Main Genre'}
                options={genreLabels}
                body={props.body}
                setBody={props.setBody}
                includesCheckbox={true}
                checkboxLabel={'Include unkowns'}
            ></MultipleSelectChipWrapper>
            <MultipleSelectChip
                title={'Language'}
                options={languageLabels}
                body={props.body}
                setBody={props.setBody}
            ></MultipleSelectChip>
        </div>
        <div className='playlist-creation'>
            <LoginButton
                text={'Login'}
                body={props.body}
                setBody={props.setBody}
            ></LoginButton>
        </div>
    </div>
}