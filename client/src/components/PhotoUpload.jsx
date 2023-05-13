import { DropzoneArea } from 'material-ui-dropzone'

export default function PhotoUpload(props) {
    function handleChange(files) {
        props.setFiles(files);
    };

    return (
        <DropzoneArea
            onChange={handleChange}
        />
    )
}
