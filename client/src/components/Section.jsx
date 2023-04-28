import { useState } from "react"
import './Section.css';

export default function Section(props) {
    const [isHidden, setIsHidden] = useState(true);

    const handleHidden = () => {
        isHidden ? setIsHidden(false) : setIsHidden(true)
    };

    const getHeader = (arrowDirection) => {
        return (
            <h5
                onClick={() => handleHidden()}>
                <i class={`arrow ${arrowDirection}`}></i>
                {props.header}
            </h5>
        )
    };
    
    if (isHidden) {
        return (
            <div className="data-section">
                {getHeader('right')}
            </div>
        )
    } else {
        return (
            <div className="data-section">
                {getHeader('down')}
                {props.sectionDetails}
            </div>
        )
    }
}
