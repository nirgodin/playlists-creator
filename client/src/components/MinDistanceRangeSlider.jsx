import * as React from 'react';
import { useState, useEffect } from "react";
import { Box, Typography } from "@mui/material";
import { Slider } from "@mui/material";

const MinDistanceRangeSlider = (props) => {
    const [minMaxValues, setminMaxValues] = useState([0, 100]);
    React.useEffect(
        () => {
            let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
            newBody['filterParams'][`min${props.title}`]['value'] = minMaxValues[0];
            newBody['filterParams'][`max${props.title}`]['value'] = minMaxValues[1];
            props.setBody([newBody]);
        }, []
    )

    const handleChange = (event, newValue, activeThumb) => {
        if (!Array.isArray(newValue)) {
            return;
        }

        if (activeThumb === 0) {
            setminMaxValues([Math.min(newValue[0], minMaxValues[1] - props.minDistance), minMaxValues[1]]);
        } else {
            setminMaxValues([minMaxValues[0], Math.max(newValue[1], minMaxValues[0] + props.minDistance)]);
        }
    };

    return (
        <Box sx={{ width: 300 }}>
            <Typography gutterBottom>{props.title}</Typography>
            <Slider
                value={minMaxValues}
                onChange={handleChange}
                valueLabelDisplay="auto"
                disableSwap
            />
        </Box>
    );
}

export default MinDistanceRangeSlider