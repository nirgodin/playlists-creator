import TextField from '@mui/material/TextField';
import { toCamelCase } from '../utils/StringUtils';
import { useState } from 'react';

export default function FormTextField(props) {
    const [value, setValue] = useState(props.defaultValue)
    const handleChange = (event) => {
        setValue(event.target.value);
        const newBody = props.body[0];
        const bodyKey = toCamelCase(props.label);
        newBody['playlistDetails'][bodyKey] = event.target.value;
        props.setBody([newBody]);
    }

    const isError = (props.isRequired && value === '') ? true : false
    const helperText = (isError) ? 'This field is required' : ''
    return <TextField
        inputProps={{ style: { color: "white" } }}
        multiline={true}
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