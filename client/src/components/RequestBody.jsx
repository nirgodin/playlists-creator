import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import MultipleSelectChip from './MultipleSelectChip';
import { languageLabels, genreLabels } from '../consts';
import { useEffect, useState } from 'react';
import SendButton from './SendButton';
import FilterCheckbox from './Checkbox';
import './RequestBody.css'
import MultipleSelectChipWrapper from './MultipleSelectChipWrapper';

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
        <MultipleSelectChipWrapper
                title={'genre'}
                options={genreLabels}
                body={body}
                setBody={setBody}
                includesCheckbox={true}
                checkboxLabel={'Include unkowns'}
        ></MultipleSelectChipWrapper>
        <MultipleSelectChip
            title={'language'}
            options={languageLabels}
            body={body}
            setBody={setBody}
        ></MultipleSelectChip>
        <SendButton text={'Create Playlist'}></SendButton>
        {/* <p>{JSON.stringify(body)}</p> */}
    </div>
}