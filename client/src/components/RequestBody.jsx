import RangeSliders from './RangeSliders';
import SelectChips from './SelectChips';

export default function RequestBody(props) {
    return <div>
        <div className='playlist-configuration'>
            <SelectChips
                body={props.body}
                setBody={props.setBody}
            ></SelectChips>
            <RangeSliders
                body={props.body}
                setBody={props.setBody}
            ></RangeSliders>
        </div>
    </div>
}