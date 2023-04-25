import { useState } from "react";
import { Box, Typography } from "@mui/material";
import { Slider } from "@mui/material";

const MinDistanceRangeSlider = (props) => {
    const handleChange = (event, newValue, activeThumb) => {
        if (!Array.isArray(newValue)) {
            return;
        }

        if (activeThumb === 0) {
            props.setValue([Math.min(newValue[0], props.value[1] - props.minDistance), props.value[1]]);
        } else {
            props.setValue([props.value[0], Math.max(newValue[1], props.value[0] + props.minDistance)]);
        }
    };

    return (
        <Box sx={{ width: 300 }}>
            <Typography gutterBottom>{props.title}</Typography>
            <Slider
                value={props.value}
                onChange={handleChange}
                valueLabelDisplay="auto"
                disableSwap
            />
        </Box>
    );
}

export default MinDistanceRangeSlider