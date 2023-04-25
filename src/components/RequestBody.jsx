import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import MultipleSelectChip from './MultiSelectChip';
import { languageLabels, genreLabels } from '../consts';
import { useState } from 'react';

export default function RequestBody() {
    const [popularityValues, setPopularityValues] = useState([0, 100]);
    
    const buildRequestBody = () => {
        const body = [
            {
                'variable': 'popularity',
                'operator': '>',
                'value': popularityValues[0]
            },
            {
                'variable': 'popularity',
                'operator': '<',
                'value': popularityValues[1]
            },
            // {
            //     'variable': 'genre',
            //     'operator': 'IN',
            //     'value': popularityValues[1]
            // },
            // {
            //     'variable': 'popularity',
            //     'operator': '<',
            //     'value': popularityValues[1]
            // },
        ]

        return JSON.stringify(body)
    }

    return <div>
        <MinDistanceRangeSlider
            minDistance={10}
            value={popularityValues}
            setValue={setPopularityValues}
            title={'Popularity'}
        ></MinDistanceRangeSlider>
        <MultipleSelectChip
            title={'Genre'}
            options={genreLabels}
        ></MultipleSelectChip>
        <MultipleSelectChip
            title={'Language'}
            options={languageLabels}
        ></MultipleSelectChip>
        <p>{buildRequestBody()}</p>
    </div>
}