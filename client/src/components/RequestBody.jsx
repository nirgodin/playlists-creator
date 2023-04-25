import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import NewMultipleSelectChip from './NewMultiSelectChip';
import { languageLabels, genreLabels } from '../consts';
import { useEffect, useState } from 'react';
import SendButton from './SendButton';

export default function RequestBody() {
    const [popularityValues, setPopularityValues] = useState([0, 100]);
    const [body, setBody] = useState(
        [
            {
                'genre': {
                    'operator': 'in',
                    'value': []
                },
                'language': {
                    'operator': 'in',
                    'value': []
                },
                'minPopularity': {
                    'operator': 'range',
                    'value': 0
                },
                'maxPopularity': {
                    'operator': '<',
                    'value': 100
                }
            }
        ]
    )

    return <div>
        <MinDistanceRangeSlider
            minDistance={10}
            value={popularityValues}
            setValue={setPopularityValues}
            title={'Popularity'}
            body={body}
            setBody={setBody}
        ></MinDistanceRangeSlider>
        <NewMultipleSelectChip
            title={'genre'}
            options={genreLabels}
            body={body}
            setBody={setBody}
        ></NewMultipleSelectChip>
        <NewMultipleSelectChip
            title={'language'}
            options={languageLabels}
            body={body}
            setBody={setBody}
        ></NewMultipleSelectChip>
        <SendButton text={'Create Playlist'}></SendButton>
        {/* <p>{JSON.stringify(body)}</p> */}
    </div>
}