import TextField from '@mui/material/TextField';
import toCamelCase from '../utils/StringUtils';

export default function FormTextField(props) {
    const handleChange = (event) => {
        const newBody = props.body;
        const bodyKey = toCamelCase(props.label);
        newBody['playlistDetails'][bodyKey] = event.target.value;
        props.setBody(newBody);
    }

    if (props.isRequired) {
        return <TextField
            required
            id={props.id}
            label={props.label}
            defaultValue={props.defaultValue}
            onChange={handleChange}
        />
    } else {
        return <TextField
            id={props.id}
            label={props.label}
            defaultValue={props.defaultValue}
            onChange={handleChange}
        />
    }
}