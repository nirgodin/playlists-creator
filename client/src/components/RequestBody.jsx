import RangeSliders from './RangeSliders';
import SelectChips from './SelectChips';
import { useEffect, useState } from 'react';
import _ from 'underscore';
import { FEATURES_DESCRIPTIONS } from '../consts';
import { sendGetRequest } from '../utils/RequestsUtils';

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
        const descriptions = await sendGetRequest(FEATURES_DESCRIPTIONS, FEATURES_DESCRIPTIONS);
        setFeaturesDescriptions(descriptions);
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