import React, { useState, useEffect, useRef } from 'react';
import p5 from 'p5';
import { createSketch } from '../Shared/TimelineSketch';

const InteractiveTimelineComponent = ({userId, showTimeline, selectedTimeline}) => {
    const sketchRef = useRef(null);
    const [screenWidth, setScreenWidth] = useState(window.innerWidth);
    const [screenHeight, setScreenHeight] = useState(window.innerHeight);


    useEffect(() => {
        console.log("TimelineComponent mounted");
        console.log("selectedTimeline: ", selectedTimeline);
        const handleResize = () => {
            setScreenWidth(window.innerWidth);
            setScreenHeight(window.innerHeight);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);



    useEffect(() => {

          const sketch = createSketch();
          const container = sketchRef.current;
          const myP5 = new p5(sketch, container)

        return () => {
            myP5.remove();
          };
    }, []);



    if (userId === null) return <div>Please select a user to view their timeline.</div>;
    if (showTimeline === null || showTimeline === undefined || showTimeline === false) return <div>Please select a user to view their timeline.</div>;
    return (
        <>         
        <div ref={sketchRef}>

        </div>      
        </>
    )
}

export default InteractiveTimelineComponent;