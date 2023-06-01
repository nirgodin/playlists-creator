import * as React from 'react';
import { Box } from '@mui/material';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import { toCamelCase } from '../utils/StringUtils';
import _ from 'underscore'
import { FILTER_PARAMS, MenuProps, POSSIBLE_VALUES, VALUE } from '../consts';
import { sendGetRequest } from '../utils/RequestsUtils';
import PropTypes from 'prop-types';

function MultipleSelectChip(props) {
    const [possibleValues, setPossibleValues] = React.useState([])

    const getPossibleValues = async () => {
        const values = await sendGetRequest(`${POSSIBLE_VALUES}/${props.title}`, POSSIBLE_VALUES);
        setPossibleValues(values);
    };

    const [selectedOptions, setSelectedOptions] = React.useState([]);

    React.useEffect(
        () => {
            if (_.isEqual(possibleValues, [])) {
                getPossibleValues()
            }
            let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
            const camelCasedTitle = toCamelCase(props.title)
            newBody[FILTER_PARAMS][camelCasedTitle][VALUE] = selectedOptions;
            props.setBody([newBody]);
        }
    )
    const handleChange = (event) => {
        const {
            target: { value },
        } = event;
        setSelectedOptions(
            typeof value === 'string' ? value.split(',') : value,
        );
    };

    return (
        <div className='multiple-select-chip'>
            <Box sx={{ width: 200 }}>
                <FormControl sx={{ width: 200 }}>
                    <InputLabel className='input-label' id="demo-multiple-chip-label" style={{color: 'white'}}>{props.title}</InputLabel>
                    <Select
                        labelId="demo-multiple-chip-label"
                        id="demo-multiple-chip"
                        multiple
                        value={selectedOptions}
                        onChange={handleChange}
                        input={<OutlinedInput id="select-multiple-chip" label={props.title} />}
                        renderValue={(selected) => (
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                {selected.map((value) => (
                                    <Chip key={value} label={value} sx={{ color: 'white' }} />
                                ))}
                            </Box>
                        )}
                        MenuProps={MenuProps}
                    >
                        {possibleValues.map((option) => (
                            <MenuItem
                                key={option}
                                value={option}
                            >
                                {option}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>
        </div>
    );
}

MultipleSelectChip.propTypes = {
    title: PropTypes.string,
    body: PropTypes.array,
    setBody: PropTypes.func
}

export default MultipleSelectChip;