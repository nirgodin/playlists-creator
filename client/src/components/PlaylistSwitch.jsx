import * as React from 'react';
import Switch from '@mui/material/Switch';
import { FormGroup, FormControlLabel } from '@mui/material';
import { IS_PUBLIC, PLAYLIST_DETAILS } from '../consts';
import PropTypes from 'prop-types';

function PlaylistSwitch(props) {
    const [label, setLabel] = React.useState('Make playlist public');
    const [checked, setChecked] = React.useState(false);

    function handleChange(event) {
        setChecked(event.target.checked);
        let newBody = props.body[0];
        newBody[PLAYLIST_DETAILS][IS_PUBLIC] = event.target.checked;
        props.setBody([newBody]);

        event.target.checked ? setLabel('Make playlist private') : setLabel('Make playlist public')
    }

    return (
        <FormGroup className='playlist-switch'>
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

PlaylistSwitch.propTypes = {
    body: PropTypes.array,
    setBody: PropTypes.func
}

export default PlaylistSwitch;