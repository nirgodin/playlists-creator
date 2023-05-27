import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import cloneJSON from '../utils/JsonUtils';
import { getFirstLetter } from '../utils/StringUtils';

export default function AutocompleteSelect(props) {
    const options = toOptions();

    function toOptions() {
        const clonedPossibleValues = cloneJSON(props.possibleValues);
        return clonedPossibleValues.map(
            value => optionifySingleValue(value)
        )
    }

    function optionifySingleValue(value) {
        const firstLetter = getFirstLetter(value);
        return {
            'firstLetter': /[0-9]/.test(firstLetter) ? '0-9' : firstLetter,
            'option': value
        }
    }

    // // const options = props.possibleValues.map((option) => {
    // const firstLetter = option.title[0].toUpperCase();
    // return {
    //     firstLetter: /[0-9]/.test(firstLetter) ? '0-9' : firstLetter,
    //     ...option,
    // };
    //   });

    return (
        <Autocomplete
            multiple
            id="grouped-demo"
            options={options.sort((a, b) => -b.firstLetter.localeCompare(a.firstLetter))}
            groupBy={(option) => option.firstLetter}
            getOptionLabel={(option) => option.option}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="With categories" />}
        />
    );
}
