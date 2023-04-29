import * as React from 'react';
import Box from '@mui/material/Box';
import FormTextField from './FormTextField';
import PlaylistSwitch from './PlaylistSwitch';

export default function PlaylistTextFields(props) {
    return (
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m: 1, width: '15ch' },
            }}
            noValidate
            autoComplete="off"
        >
            <div className='is-public-switch'>
                <PlaylistSwitch
                    body={props.body}
                    setBody={props.setBody}
                ></PlaylistSwitch>
            </div>
            <div>
                <FormTextField
                    isRequired={true}
                    id={'playlist-name'}
                    label={"Playlist name"}
                    defaultValue={''}
                    body={props.body}
                    setBody={props.setBody}
                ></FormTextField>
                <FormTextField
                    isRequired={false}
                    id={'playlist-description'}
                    label={"Playlist description"}
                    defaultValue={''}
                    body={props.body}
                    setBody={props.setBody}
                ></FormTextField>
            </div>
        </Box>
    );
}