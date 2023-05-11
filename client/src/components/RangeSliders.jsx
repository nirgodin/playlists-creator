import MinDistanceRangeSliderWrapper from "./MinDistanceRangeSliderWrapper";
import _ from "underscore";
import axios from "axios";
import { useState, useEffect } from "react"

export default function RangeSliders(props) {
    const [featuresNames, setFeaturesNames] = useState([])

    async function getFeaturesNames() {
        const url = `${process.env.REACT_APP_BASE_URL}/featuresNames/minMaxValues`;
        await axios.get(url)
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => jsonfiedData['featuresNames'])
            .then((featuresNames) => setFeaturesNames(featuresNames))
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