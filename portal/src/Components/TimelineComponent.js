import React, { useState, useEffect, useRef } from 'react';
import { DataSet, Timeline } from 'vis-timeline/standalone';
import { Box, Typography, Button, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import axios from 'axios';
import PhotoIcon from '@mui/icons-material/Photo';

const TimelineComponent = ({userId, showTimeline}) => {
    const timelineRef = useRef(null);
    const [milestonesFetched, setMilestonesFetched] = useState(false);
    const [screenWidth, setScreenWidth] = useState(window.innerWidth + 'px');
    const [screenHeight, setScreenHeight] = useState(window.innerHeight + 'px');
    const [milestoneData, setMilestoneData] = useState([]);
    const [selectedMilestone, setSelectedMilestone] = useState(null);
    const [timeline, setTimeline] = useState(null);
    const [openDialog, setOpenDialog] = useState(false);

    useEffect(() => {
        console.log("TimelineComponent mounted");
        console.log("window.innerWidth:", screenWidth);
        console.log("window.innerHeight:", screenHeight);
        const handleResize = () => {

            setScreenWidth(window.innerWidth + 'px');
            setScreenHeight(window.innerHeight + 'px');
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    useEffect(() => {
        if (showTimeline && !milestonesFetched && timelineRef.current) {
            fetchTimeLineData();
        }
    }, [showTimeline, userId]);

    useEffect(() => {
        const handleSelectedTimelineEvent = (properties) => {
            console.log("selected timeline event:", properties);
            console.log("selected milestone:", selectedMilestone);
            if(properties.items.length < 1 || (selectedMilestone && selectedMilestone.id !== properties.items[0])){   
                console.log("setting selected milestone to null");             
                setSelectedMilestone(null);
                
            }else{
                const sm = milestoneData.find(milestone => milestone.id === properties.items[0]);
                if (sm) {
                    setSelectedMilestone(sm);
                    setOpenDialog(true);
                }
            }
 
        };
        if (timeline) {            
            timeline.on('select', handleSelectedTimelineEvent);
        }
    }, [milestoneData]);



    const fetchTimeLineData = async () => {
        try{
            console.log("fetching timeline data for user:", userId);
            const response = await axios.get('http://127.0.0.1:8000/insta-user/user-timeline/' + userId);
            //const response = {data:{ "milestones": [{"id": 0, "title": "Birth", "description": "You were born on a unique leap day, February 29, 1996.", "date": "1996-02-29", "significance": "Significant as it adds a unique aspect to your life."}, {"id": 1, "title": "First Memory", "description": "A cherished moment with your mom in your first house in Ruidoso. You rode your scooter around the neighborhood, and you both walked down a giant hill back to your home.", "date": "1999-01-01", "significance": "This memory reflects the joy of childhood and the bond with your mother."}, {"id": 2, "title": "Move to Euless, Texas", "description": "At the age of 5, you moved to Euless, Texas, starting a new chapter in your life.", "date": "2001-01-01", "significance": "This move represents a significant transition in your life."}]}}
            console.log("fetched timeline data:", response.data);
            const milestones = response.data.milestones;
            setMilestoneData(milestones);
            const container = timelineRef.current;
            const milestoneData = milestones.map(milestone => {
                const md = {
                    id: milestone.id,
                    content: milestone.title,
                    start: milestone.start_date,
                    title: milestone.description,
                    
                }
                if(milestone.end_date){
                    md.end = milestone.end_date;
                    md.type = 'range';
                    md.style = 'background-color: #FFE4E1;';
                }
                if(milestone.importance){
                    md.group = milestone.importance
                }else{
                    md.group = "unknown"
                }
                
                if(milestone.images){
                    console.log(milestone.images);
                    const photoIconSvg = `<img src="/mui_image_icon.svg" alt="Image Included" style="width: 20px; height: 20px; margin-left: 8px;"/>`
                    md.content = `
                        <div>${milestone.title}</div>
                        <span>${photoIconSvg}</span>
                        `
                    console.log(md.content)
                }
                
              
                return md
            });
            const items = new DataSet(milestoneData);
            const options = {};
            var groups = [
                {
                    id: "high",
                    content: 'High Importance',
                    style: 'color: black; background-color:rgba(170, 240, 209,0.5);',
                    title: 'This is group 1'
                  },{
                  id: "medium",
                  content: 'Medium Importance',
                  style: 'color: black; background-color: rgba(170, 240, 209,0.5);',
                  title: 'This is group 2'
                },
                {
                    id: "low",
                    content: 'Low Importance',
                    style: 'color: black; background-color: rgba(170, 240, 209,0.5);',
                    title: 'This is group 3'
                  },
                {
                    id: "unknown",
                    content: 'Misc',
                    style: 'color: black; background-color: rgba(170, 240, 209,0.5);',
                    title: 'This is group 4'
                  }
              ];
            const tl = new Timeline(container, items, groups, options);
            setTimeline(tl);
            setMilestonesFetched(true);

        }catch(error){
            console.error('Error fetching timeline data:', error);
        }
    }

    
    const handleCloseDialog = () => {
        console.log("closing dialog");
        setOpenDialog(false);
        setSelectedMilestone(null);
      
    };

    useEffect(() => {
        const style = document.createElement('style');
        style.innerHTML = `
            .vis-item-content {
                display: flex;
                align-items: center;
                justify-content: center;
            }
        `;
        document.head.appendChild(style);
    }, []);

    if (userId === null) return <div>Please select a user to view their timeline.</div>;
        
    return (
        <>
        {/* <script type="text/javascript" src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
        <link href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet" type="text/css" /> */}

        {showTimeline && (
            <Box sx={{width:'100%'}}>
                <div id="visualization" ref={timelineRef} style={{width: '100%', border: '1px solid lightgray' }}></div>
                
                {selectedMilestone && (
                    <Dialog open={openDialog} onClose={handleCloseDialog}>
                        <DialogTitle>Selected Milestone</DialogTitle>
                        <DialogContent>
                            {selectedMilestone && (
                                <>
                                    <Typography variant="body1">
                                        <strong>Title:</strong> {selectedMilestone.title}
                                    </Typography>
                                    <Typography variant="body1">
                                        <strong>Description:</strong> {selectedMilestone.description}
                                    </Typography>
                                    
                                    {(selectedMilestone.end_date === null || selectedMilestone.end_date === "") && (
                                        <Typography variant="body1">
                                        <strong>Date:</strong> {selectedMilestone.start_date}
                                    </Typography>
                                    )}
                                    {selectedMilestone.end_date && (
                                        <>
                                        <Typography variant="body1">
                                        <strong>Start Date:</strong> {selectedMilestone.start_date}
                                        </Typography>
                                        <Typography variant="body1">
                                            <strong>End Date:</strong> {selectedMilestone.end_date}
                                        </Typography>
                                        </>
                                    )}
                                    <Typography variant="body1">
                                        <strong>Significance:</strong> {selectedMilestone.significance}
                                    </Typography>
                                    {selectedMilestone.location && (      
                                    <Typography variant="body1">
                                        <strong>Location:</strong> {selectedMilestone.location}
                                    </Typography>
                                    )}
                                     {selectedMilestone.images && selectedMilestone.images.length > 0 && (
                                        selectedMilestone.images.map((image, index) => (
                                            <img
                                                key={index}
                                                src={`data:image/png;base64,${image}`}
                                                style={{ width: '200px', height: '200px', borderRadius: '5%', margin: '10px' }}
                                                alt={`Milestone Image ${index + 1}`}
                                            />
                                        ))
                                        )}
                                </>
                            )}
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleCloseDialog} color="primary">
                                Close
                            </Button>
                        </DialogActions>
                    </Dialog>
                
                )}
                </Box>
            )}
                
        </>
    )
}

export default TimelineComponent;