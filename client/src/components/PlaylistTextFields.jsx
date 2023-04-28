import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import FormTextField from './FormTextField';

export default function PlaylistTextFields(props) {
    return (
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m: 1, width: '25ch' },
            }}
            noValidate
            autoComplete="off"
        >
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
                    isRequired={true}
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