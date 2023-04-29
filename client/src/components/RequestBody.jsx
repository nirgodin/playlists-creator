import MinDistanceRangeSlider from './MinDistanceRangeSlider';
import MultipleSelectChip from './MultipleSelectChip';
import { languageLabels, genreLabels } from '../consts';
import MultipleSelectChipWrapper from './MultipleSelectChipWrapper';
import AudioFeaturesSliders from './AudioFeaturesSliders';
import Section from './Section';

export default function RequestBody(props) {
    return <div>
        <div className='playlist-configuration'>
            <Section
                header='Audio Features'
                sectionDetails={
                    <AudioFeaturesSliders
                        body={props.body}
                        setBody={props.setBody}
                    ></AudioFeaturesSliders>
                }
            ></Section>
            <MinDistanceRangeSlider
                minDistance={10}
                title={'Popularity'}
                body={props.body}
                setBody={props.setBody}
            ></MinDistanceRangeSlider>
            <MultipleSelectChipWrapper
                title={'Main Genre'}
                options={genreLabels}
                body={props.body}
                setBody={props.setBody}
                includesCheckbox={true}
                checkboxLabel={'Include unkowns'}
            ></MultipleSelectChipWrapper>
            <MultipleSelectChip
                title={'Language'}
                options={languageLabels}
                body={props.body}
                setBody={props.setBody}
            ></MultipleSelectChip>
        </div>
    </div>
}