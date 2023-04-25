import { useState } from "react";
import { Box, Typography } from "@mui/material";
import { Slider } from "@mui/material";

const MinDistanceRangeSlider = (props) => {
    const [value, setValue] = useState(props.value);

    const handleChange = (event, newValue, activeThumb) => {
        if (!Array.isArray(newValue)) {
            return;
        }

        if (activeThumb === 0) {
            setValue([Math.min(newValue[0], value[1] - props.minDistance), value[1]]);
        } else {
            setValue([value[0], Math.max(newValue[1], value[0] + props.minDistance)]);
        }
    };

    return (
        <Box sx={{ width: 300 }}>
            <Typography gutterBottom>{props.label}</Typography>
            <Slider
                value={value}
                onChange={handleChange}
                valueLabelDisplay="auto"
                disableSwap
            />
        </Box>
    );
}

export default MinDistanceRangeSlider