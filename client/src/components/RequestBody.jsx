import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import MultipleSelectChip from './MultiSelectChip';
import NewMultipleSelectChip from './NewMultiSelectChip';
import { languageLabels, genreLabels } from '../consts';
import { useEffect, useState } from 'react';

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
                'popularity': {
                    'operator': 'range',
                    'value': ''
                }
            }
        ]
    )

    return <div>
        <MinDistanceRangeSlider
            minDistance={10}
            value={popularityValues}
            setValue={setPopularityValues}
            title={'popularity'}
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
        {/* <p>{JSON.stringify(body)}</p> */}
    </div>
}