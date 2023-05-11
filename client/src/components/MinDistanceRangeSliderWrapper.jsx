import InfoToolTip from "./InfoToolTip";
import MinDistanceRangeSlider from "./MinDistanceRangeSlider";

export default function MinDistanceRangeSliderWrapper(props) {
    return (
        <div className="range-slider-wrapper">
            <div className='row-items'>
                <InfoToolTip
                    featuresDescriptions={props.featuresDescriptions}
                    title={props.title}
                ></InfoToolTip>
                <MinDistanceRangeSlider
                    title={props.featureName}
                    body={props.body}
                    setBody={props.setBody}
                ></MinDistanceRangeSlider>
            </div>
        </div>
    )
};