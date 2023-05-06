import MultipleSelectChipWrapper from './MultipleSelectChipWrapper';
import RangeSliders from './RangeSliders';
import SelectChips from './SelectChips';

export default function RequestBody(props) {
    return <div>
        <div className='playlist-configuration'>
            <RangeSliders
                body={props.body}
                setBody={props.setBody}
            ></RangeSliders>
            <SelectChips
                body={props.body}
                setBody={props.setBody}
            ></SelectChips>
            {/* <p>{JSON.stringify(props.body[0])}</p> */}
        </div>
    </div>
}