import TextField from '@mui/material/TextField';
import {toCamelCase} from '../utils/StringUtils';
import { useState } from 'react';

export default function FormTextField(props) {
    const [value, setValue] = useState(props.defaultValue)
    // useEffect(
    //     () => {
    //         if (props.isRequired && )
    //     }
    // )
    // const [isError, setIsError] = useState()
    const handleChange = (event) => {
        setValue(event.target.value);
        const newBody = props.body;
        const bodyKey = toCamelCase(props.label);
        newBody['playlistDetails'][bodyKey] = event.target.value;
        props.setBody(newBody);
    }

    const isError = (props.isRequired && value === '') ? true : false
    const helperText = (isError) ? 'This field is required' : ''
    return <TextField
        error={isError}
        required={props.isRequired}
        value={value}
        id={props.id}
        label={props.label}
        defaultValue={props.defaultValue}
        onChange={handleChange}
        helperText={helperText}
    />
}