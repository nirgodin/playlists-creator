import InfoToolTip from "./InfoToolTip";
import MinDistanceRangeSlider from "./MinDistanceRangeSlider";

export default function MinDistanceRangeSliderWrapper(props) {
    return (
        <div className="range-slider-wrapper">
            <div className='row-items'>
                <div className="range-slider-tooltip">
                    <InfoToolTip
                        featuresDescriptions={props.featuresDescriptions}
                        title={props.title}
                    ></InfoToolTip>
                </div>
                <div className="slider">
                    <MinDistanceRangeSlider
                        title={props.title}
                        body={props.body}
                        setBody={props.setBody}
                    ></MinDistanceRangeSlider>
                </div>
            </div>
        </div>
    )
};