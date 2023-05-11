import RangeSliders from './RangeSliders';
import SelectChips from './SelectChips';
import axios from 'axios';
import { useEffect, useState } from 'react';
import _ from 'underscore';
import { FEATURES_DESCRIPTIONS } from '../consts';

export default function RequestBody(props) {
    const [featuresDescriptions, setFeaturesDescriptions] = useState([]);

    useEffect(
        () => {
          if (_.isEqual(featuresDescriptions, [])) {
            setDescriptions();
          }
        }, [featuresDescriptions]
      )
    
    async function setDescriptions() {
        const url = `${process.env.REACT_APP_BASE_URL}/${FEATURES_DESCRIPTIONS}`;
        await axios.get(url)
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => jsonfiedData[FEATURES_DESCRIPTIONS])
            .then((descriptions) => setFeaturesDescriptions(descriptions))
    }

    return <div>
        <div className='playlist-configuration'>
            <SelectChips
                body={props.body}
                setBody={props.setBody}
                featuresDescriptions={featuresDescriptions}
            ></SelectChips>
            <RangeSliders
                body={props.body}
                setBody={props.setBody}
                featuresDescriptions={featuresDescriptions}
            ></RangeSliders>
        </div>
    </div>
}