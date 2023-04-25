import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import MultipleSelectChip from './MultiSelectChip';
import { languageLabels, genreLabels } from '../consts';
import { useState } from 'react';

export default function RequestBody() {
    const [popularityValues, setPopularityValues] = useState([0, 100]);
    const [genreValues, setGenresValues] = useState([]);
    const [languageValues, setLanguageValues] = useState([]);

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
            {
                'variable': 'genre',
                'operator': 'in',
                'value': genreValues
            },
            {
                'variable': 'language',
                'operator': 'in',
                'value': languageValues
            },
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
            selectedOptions={genreValues}
            setSelectedOptions={setGenresValues}
        ></MultipleSelectChip>
        <MultipleSelectChip
            title={'Language'}
            options={languageLabels}
            selectedOptions={languageValues}
            setSelectedOptions={setLanguageValues}
        ></MultipleSelectChip>
        {/* <p>{buildRequestBody()}</p> */}
    </div>
}