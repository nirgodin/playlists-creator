import * as React from 'react';
import { Box } from '@mui/material';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import { toCamelCase } from '../utils/StringUtils';
import axios from 'axios'
import _ from 'underscore'

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
            backgroundColor: 'rgb(0, 30, 60)',
            color: 'white',
        },
    },
};

export default function MultipleSelectChip(props) {
    const [possibleValues, setPossibleValues] = React.useState([])

    const getPossibleValues = async () => {
        const url = `${process.env.REACT_APP_BASE_URL}/possibleValues/${props.title}`;
        await axios.get(url)
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => jsonfiedData['possibleValues'])
            .then((values) => setPossibleValues(values))
    };

    const [selectedOptions, setSelectedOptions] = React.useState([]);

    React.useEffect(
        () => {
            if (_.isEqual(possibleValues, [])) {
                getPossibleValues()
            }
            let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
            const camelCasedTitle = toCamelCase(props.title)
            newBody['filterParams'][camelCasedTitle]['value'] = selectedOptions;
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