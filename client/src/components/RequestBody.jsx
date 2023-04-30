import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import MultipleSelectChip from './MultipleSelectChip';
import { languageLabels, genreLabels } from '../consts';
import MultipleSelectChipWrapper from './MultipleSelectChipWrapper';
import AudioFeaturesSliders from './AudioFeaturesSliders';
import Section from './Section';

export default function RequestBody(props) {
    return <div>
        <div className='playlist-configuration'>
            <AudioFeaturesSliders
                body={props.body}
                setBody={props.setBody}
            ></AudioFeaturesSliders>
            {/* <Section
                header='Audio Features'
                sectionDetails={
                    <AudioFeaturesSliders
                        body={props.body}
                        setBody={props.setBody}
                    ></AudioFeaturesSliders>
                }
            ></Section> */}
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