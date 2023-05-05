import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import MultipleSelectChipWrapper from './MultipleSelectChipWrapper';
import RangeSliders from './RangeSliders';

export default function RequestBody(props) {
    return <div>
        <div className='playlist-configuration'>
            <RangeSliders
                body={props.body}
                setBody={props.setBody}
            ></RangeSliders>
            <MinDistanceRangeSlider
                minDistance={10}
                title={'Popularity'}
                body={props.body}
                setBody={props.setBody}
            ></MinDistanceRangeSlider>
            <MultipleSelectChipWrapper
                title={'Main Genre'}
                body={props.body}
                setBody={props.setBody}
                includesCheckbox={true}
                checkboxLabel={'Include unkowns'}
            ></MultipleSelectChipWrapper>
            <MultipleSelectChipWrapper
                title={'Language'}
                body={props.body}
                setBody={props.setBody}
                includesCheckbox={true}
                checkboxLabel={'Include unkowns'}
            ></MultipleSelectChipWrapper>
        </div>
    </div>
}