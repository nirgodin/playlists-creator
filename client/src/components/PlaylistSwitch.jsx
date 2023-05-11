import * as React from 'react';
import Switch from '@mui/material/Switch';
import { FormGroup, FormControlLabel } from '@mui/material';
import { PLAYLIST_DETAILS } from '../consts';

export default function PlaylistSwitch(props) {
    const [label, setLabel] = React.useState('Make playlist public');
    const [checked, setChecked] = React.useState(false);

    const handleChange = (event) => {
        setChecked(event.target.checked);
        let newBody = props.body[0];
        newBody[PLAYLIST_DETAILS]['isPublic'] = event.target.checked;
        props.setBody([newBody]);

        event.target.checked ? setLabel('Make playlist private') : setLabel('Make playlist public')
    };

    return (
        <FormGroup>
            <FormControlLabel
                control={
                    <Switch
                        checked={checked}
                        onChange={handleChange}
                        size='small'
                    />
                }
                label={label}
            />
        </FormGroup>
    );
}