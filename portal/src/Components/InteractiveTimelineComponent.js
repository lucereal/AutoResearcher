import React, { useState, useEffect, useRef } from 'react';

import p5 from 'p5';

const InteractiveTimelineComponent = ({userId, showTimeline}) => {
    const sketchRef = useRef(null);
    const [milestonesFetched, setMilestonesFetched] = useState(false);
    const [screenWidth, setScreenWidth] = useState(window.innerWidth);
    const [screenHeight, setScreenHeight] = useState(window.innerHeight);
    const [milestoneData, setMilestoneData] = useState([]);
    const [selectedMilestone, setSelectedMilestone] = useState(null);
    const [timeline, setTimeline] = useState(null);
    const [openDialog, setOpenDialog] = useState(false);
    const [myP5, setMyP5] = useState(null);

    useEffect(() => {
        console.log("TimelineComponent mounted");
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
        if (showTimeline && userId && !myP5) {
            console.log("Creating timeline...");
            setUpP5();
        }
    }, [showTimeline, userId, myP5]);

    const createSketch = () => {
        const sketch = (p) => {
            p.setup = () => {
                p.createCanvas(screenWidth, screenHeight);
                p.background(255);
            };
            p.draw = () => {
                p.fill(0);
                p.ellipse(p.mouseX, p.mouseY, 20, 20);
            };
        };
        return sketch;
    }

    const setUpP5 = () => {
        const sketch = createSketch();
        const container = sketchRef.current;
        const myP5 = new p5(sketch, container)
        setMyP5(myP5);
    };
  

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