import React, { useState, useEffect, useRef } from 'react';
import p5 from 'p5';
import { createSketch } from '../Shared/TimelineSketch';
import { forceDirectedGraphSketch } from '../Shared/ForceDirectedGraph';
import {storyGraphSketch} from '../Shared/StoryGraph';

const InteractiveTimelineComponent = ({userId, showTimeline, selectedTimeline}) => {
    const sketchRef = useRef(null);
    const [myP5Instance, setMyP5Instance] = useState(null);


    useEffect(() => {

        if(myP5Instance){
            console.log("removing p5 instance")
            myP5Instance.remove();
        }

        console.log("already selected timeline: ", selectedTimeline)

        let sketch;
        if(selectedTimeline === "interactiveTimeline"){
            sketch = createSketch();
        }else if(selectedTimeline === "interactiveGraph"){
            sketch = forceDirectedGraphSketch();
        }else if(selectedTimeline === "storyGraph"){
            sketch = storyGraphSketch();
        }
    
        const container = sketchRef.current;
        console.log("creating p5 instance")
        const myP5 = new p5(sketch, container)
        setMyP5Instance(myP5);
        

        return () => {
            if(myP5){
                console.log("returning remove p5")
                myP5.remove();
                
                // Manually remove the canvas element if it still exists
                if (container && container.firstChild) {
                    container.removeChild(container.firstChild);
                }
            }
          };
    }, [selectedTimeline]);



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