import MinDistanceRangeSliderWrapper from "./MinDistanceRangeSliderWrapper";
import _ from "underscore";
import { useState, useEffect } from "react"
import { FEATURES_NAMES, MIN_MAX_VALUES } from "../consts";
import { sendGetRequest } from "../utils/RequestsUtils";

export default function RangeSliders(props) {
    const [featuresNames, setFeaturesNames] = useState([])

    async function getFeaturesNames() {
        const featuresNames = await sendGetRequest(`${FEATURES_NAMES}/${MIN_MAX_VALUES}`, FEATURES_NAMES);
        setFeaturesNames(featuresNames);
    }

    useEffect(
        () => {
            if (_.isEqual(featuresNames, [])) {
                getFeaturesNames()
            }
        }, [featuresNames, setFeaturesNames]
    )

    const toRangeSliders = () => {
        if (!_.isEqual(featuresNames, [])) {
            return featuresNames.map(
                featureName => <MinDistanceRangeSliderWrapper
                    title={featureName}
                    body={props.body}
                    setBody={props.setBody}
                    featuresDescriptions={props.featuresDescriptions}
                ></MinDistanceRangeSliderWrapper>
            )
        }
    }

    return <div className="range-sliders">
        {toRangeSliders()}
    </div>
}