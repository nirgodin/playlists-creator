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

// class PhotoUpload extends Component {
//     constructor(props) {
//         super(props);
//         this.state = {
//             files: []
//         };
//     }
//     handleChange(files) {
//         this.setState({
//             files: files
//         });
//     }
//     render() {
//         return (
//             <DropzoneArea
//                 onChange={this.handleChange.bind(this)}
//             />
//         )
//     }
// }

