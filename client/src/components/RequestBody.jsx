import RangeSliders from './RangeSliders';
import SelectChips from './SelectChips';
import axios from 'axios';
import { useEffect, useState } from 'react';
import _ from 'underscore';

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
        const url = `${process.env.REACT_APP_BASE_URL}/featuresDescriptions`;
        await axios.get(url)
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => jsonfiedData['featuresDescriptions'])
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