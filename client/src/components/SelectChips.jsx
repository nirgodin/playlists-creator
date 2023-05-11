import { useState, useEffect } from "react"
import MultipleSelectChipWrapper from "./MultipleSelectChipWrapper"
import _ from "underscore";
import axios from "axios";
import { FEATURES_NAMES, POSSIBLE_VALUES } from "../consts";

export default function SelectChips(props) {
    const [featuresNames, setFeaturesNames] = useState([])

    async function getFeaturesNames() {
        const url = `${process.env.REACT_APP_BASE_URL}/${FEATURES_NAMES}/${POSSIBLE_VALUES}`;
        await axios.get(url)
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => jsonfiedData[FEATURES_NAMES])
            .then((featuresNames) => setFeaturesNames(featuresNames))
    }

    useEffect(
        () => {
            if (_.isEqual(featuresNames, [])) {
                getFeaturesNames()
            }
        }, [featuresNames, setFeaturesNames]
    )

    function toSelectChips() {
        return featuresNames.map(
            featureName => <MultipleSelectChipWrapper
                title={featureName}
                body={props.body}
                setBody={props.setBody}
                includesCheckbox={true}
                checkboxLabel={'Include unkowns'}
                featuresDescriptions={props.featuresDescriptions}
            ></MultipleSelectChipWrapper>
        )
    }

    return <div className="select-chips">
        {toSelectChips()}
    </div>
}