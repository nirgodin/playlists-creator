import React from "react";
import InfoToolTip from "./InfoToolTip";
import MinDistanceRangeSlider from "./MinDistanceRangeSlider";
import PropTypes from 'prop-types';

function MinDistanceRangeSliderWrapper(props) {
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
}

MinDistanceRangeSliderWrapper.propTypes = {
    title: PropTypes.string,
    featuresDescriptions: PropTypes.array,
    body: PropTypes.array,
    setBody: PropTypes.func
}

export default MinDistanceRangeSlider;