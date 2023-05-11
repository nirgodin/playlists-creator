import * as React from 'react';
import { useState } from "react";
import { Box, Typography } from "@mui/material";
import { Slider } from "@mui/material";
import axios from 'axios'
import _ from 'underscore'
import { toCamelCase } from '../utils/StringUtils';

const MinDistanceRangeSlider = (props) => {
    const [minMaxValues, setminMaxValues] = useState([]);
    const [actualValues, setActualValues] = useState([]);
    const [minDistance, setMinDistance] = useState(0);
    const minTitleValue = toCamelCase(`min ${props.title}`);
    const maxTitleValue = toCamelCase(`max ${props.title}`);

    const getMinMaxValues = async () => {
        if (_.isEqual(minMaxValues, [])) {
            const url = `${process.env.REACT_APP_BASE_URL}/minMaxValues/${props.title}`;
            await axios.get(url)
                .then((resp) => JSON.stringify(resp.data))
                .then((data) => JSON.parse(data))
                .then((jsonfiedData) => jsonfiedData['minMaxValues'])
                .then((values) => setminMaxValues(values))
        }
    };

    React.useEffect(
        () => {
            if (_.isEqual(minMaxValues, [])) {
                getMinMaxValues();
            }

            if (_.isEqual(actualValues, []) && !_.isEqual(minMaxValues, [])) {
                const updatedMinDistance = (minMaxValues[1] - minMaxValues[0]) / 10;
                setMinDistance(updatedMinDistance);
                setActualValues(minMaxValues);
            }
        }, [minMaxValues, actualValues, getMinMaxValues]
    )

    const updateRangeValues = (newValue, activeThumb) => {
        if (!Array.isArray(newValue)) {
            return;
        }

        if (activeThumb === 0) {
            const minActualValue = Math.min(newValue[0], actualValues[1] - minDistance);
            setActualValues([minActualValue, actualValues[1]]);
        } else {
            const maxActualValue = Math.max(newValue[1], actualValues[0] + minDistance);
            setActualValues([actualValues[0], maxActualValue]);
        }
    }

    const updateRequestBody = () => {
        let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
        newBody['filterParams'][minTitleValue]['value'] = actualValues[0];
        newBody['filterParams'][maxTitleValue]['value'] = actualValues[1];
        props.setBody([newBody]);
    }

    const handleChange = (event, newValue, activeThumb) => {
        updateRangeValues(newValue, activeThumb)
        updateRequestBody()
    };

    return (
        <div className='range-slider'>
            <Box sx={{ width: 180 }}>
                <Typography gutterBottom>{props.title}</Typography>
                <Slider
                    min={minMaxValues[0]}
                    max={minMaxValues[1]}
                    value={actualValues}
                    onChange={handleChange}
                    valueLabelDisplay="auto"
                    disableSwap
                />
            </Box>
        </div>
    );
}

export default MinDistanceRangeSlider