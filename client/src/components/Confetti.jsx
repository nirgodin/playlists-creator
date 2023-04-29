import { useEffect, useState } from 'react'
import ReactConfetti from 'react-confetti'

export default function Confetti() {
    const [windowDimension, setWindowDimension] = useState(
        {
            width: window.innerWidth,
            height: window.innerHeight
        }
    );
    
    const detcetSize = () => {
        setWindowDimension(
            {
                width: window.innerWidth,
                height: window.innerHeight
            }
        )
    }

    useEffect(
        () => {
            window.addEventListener('resize', detcetSize)
            return () => {
                window.removeEventListener('resize', detcetSize)
            }
        }, [windowDimension]
    )

    return (
        <>
            <ReactConfetti
                width={windowDimension.width}
                height={windowDimension.height}
                tweenDuration={1000}
            ></ReactConfetti>
        </>
    )

}