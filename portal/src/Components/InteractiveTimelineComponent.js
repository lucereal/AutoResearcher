import React, { useState, useEffect, useRef } from 'react';

import p5 from 'p5';
import { use } from 'react';


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
    const [timeSlider, setTimeSlider] = useState(null);




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

        let currentTitle = "";
        let currentBody = "";
        let currentImgID = null;
        let images = [];
        let ts = null;
        let sliderValue = 25;

        const displayYear = (p, ts) => {
            p.fill(0);
            p.textAlign(p.CENTER);
            p.noStroke();
            p.textSize(40);
            p.text(1750 + p.int(ts.value()), p.width / 2, 50);
        }
        
        const displayText = (p) => {

            p.textSize(20);
            p.text(currentTitle, 0, 60, 360, 90);
            p.textSize(16);
            p.textAlign(p.LEFT);
            p.text(currentBody, 0, 140, 360, 640);
        }
        
        const displayLine = (p) => {
            p.stroke(0);
            p.strokeWeight(3);
            p.line(0, 350, p.width, 350);
        }
        
        const displayIncrements = (p, ts) => {
            //draws vertical marks on line to convey movement
            p.stroke(0);
            for (var i = 0; i < 51; i++){
                p.line(i * 25 - (ts.value() * 400) % 400, 340, i * 25 - (ts.value() * 400) % 400, 360);
            }
                
        }

        const createSketch = () => {
        
            return (p) => {
    
                p.preload = () => {
                    const imgs = [p.loadImage("timeline_images/some_image.png")]
                    images = imgs;
                }   
                p.setup = () => {
                    p.createCanvas(screenWidth, screenHeight);
                    ts = p.createSlider(0, 50, 25, 1);
                    ts.input(() => {
                        sliderValue = ts.value();
                    });
    
                    ts.position(screenWidth / 2 - 362.5, screenHeight - 20); //center timeline
                    ts.style('width', '700px');
                    setTimeSlider(ts);
                };
                p.draw = () => {
                    console.log("in draw");
                    p.background(255);
    
                    displayLine(p, ts); //horizontal line in timeline
                    displayYear(p, ts); //year display on top
                    
                    displayImage(p);
                    displayIncrements(p, ts);
                      //put events on line. see event function.
                    event(p,'The French and Indian War Ends\nFeb 10 1763',
                        'The French and Indian War ends. The UK is heavily in debt and begins to expect the colonies to help pay that debt, since the war resuced them from the French. This is important because the citizens of the US had no say in how they would be charged.',
                        1763, 0, false);
                    event(p,'Stamp Act\nMar 22 1765','Parliament imposes the Stamp Act on the colonies. Major protests against "taxation without representation" start. This is important because the citizens of the US resisted unfair taxation for the first significant time'
                        ,1765,0,true);
                    
                    displayText(p, ts); //displays title and body on left
                };
            };
            
        }
        const event = (p, caption, body, year, imageID, up) => {
            let xOffs = p.width / 2 + (year-1775)*400 + (25 - ts.value()) * 400; //offset to line up with moving line
            p.noStroke();
            p.textSize(12);
            p.textAlign(p.CENTER);
            p.text(caption, xOffs, up ? 320 : 380); //puts caption above or below line
            p.fill(0, 115, 200);
            p.ellipse(xOffs, 350, 15, 15); //blue mouseover thingy
            if (p.dist(p.mouseX, p.mouseY, xOffs, 350) < 50) { //checks if mouse is close (20px) to blue thingy
                currentTitle = caption;
                currentBody = body;
                currentImgID = imageID;
            }
            p.fill(0);
          }
    
          const displayImage = (p) => {
            p.imageMode(p.CENTER);
            if (currentImgID != null) //check if any image has been selected
              if (images[currentImgID].width > images[currentImgID].height)
                //if width bigger, scale based on amount width decreased
                p.image(images[currentImgID], 540, 170, 200, (200 / images[currentImgID].width) * images[currentImgID].height);
              else
                //if height bigger, scale based on amount height decreased
                p.image(images[currentImgID], 540, 170, (200 / images[currentImgID].height) * images[currentImgID].width, 200);
          }
          
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