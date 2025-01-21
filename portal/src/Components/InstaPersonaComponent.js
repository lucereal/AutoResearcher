import React, { useState, useEffect } from 'react';
import { Box, Typography, Container, Link, Button,
  Dialog, DialogTitle, DialogContent, DialogActions, TextField,
  FormControl, InputLabel, Select, MenuItem
 } from '@mui/material';
import axios from 'axios';
import { Graph, DefaultLink, DefaultNode } from '@visx/network';
import testData from '../testdata/graph_test_data.json'; // Import the test data
import ChatComponent from './ChatComponent';
import PersonIcon from '@mui/icons-material/Person'; // Import an icon
import TimelineComponent from './TimelineComponent';
import InteractiveTimelineComponent from './InteractiveTimelineComponent';


const InstaPersonaComponent = () => {
    const [email, setEmail] = useState('');
    const [showWordGraph, setShowWordGraph] = useState(false);
    const [wordGraphData, setWordGraphData] = useState(null);
    const [nodeMultiplier, setNodeMultiplier] = useState(100);
    const [screenWidth, setScreenWidth] = useState(window.innerWidth);
    const [screenHeight, setScreenHeight] = useState(window.innerHeight);
    const [openChatDialog, setOpenChatDialog] = useState(false); // State variable to manage chat visibility
    const [showTimeline, setShowTimeline] = useState(false); // State variable to control the visibility of TimelineComponent
    const [currentUserId, setCurrentUserId] = useState(null); // State variable to store the current user ID
    const [userTimelineStory, setUserTimelineStory] = useState(null);
    const [openTimelineStoryDialog, setOpenTimelineStoryDialog] = useState(false); // State variable to control the visibility of TimelineComponent
    const [showInteractiveTimeline, setShowInteractiveTimeline] = useState(false); // State variable to control the visibility of InteractiveTimelineComponent
    const [timelineSelectedComponent, setTimelineSelectedComponent] = useState(null); // State variable to store the selected component

    useEffect(() => {
      console.log("InstaPersonaComponent mounted");
      const handleResize = () => {
          setScreenWidth(window.innerWidth);
          setScreenHeight(window.innerHeight);
      };

      window.addEventListener('resize', handleResize);

      return () => {
          window.removeEventListener('resize', handleResize);
      };
  }, []);

    const handleOpenChat = () => {
      setOpenChatDialog(!openChatDialog);
    };

   const handleOpenTimeline = () => {
    setCurrentUserId(localStorage.getItem('userId') || null)
    setShowTimeline(!showTimeline)
  }

  const handleTimelineSelectedComponentChange = (event) => {
        let selectedComponent = event.target.value;
        console.log("Selected Component:", event.target.value);
        setTimelineSelectedComponent(selectedComponent);
        if(selectedComponent === null || selectedComponent === undefined || selectedComponent === "" || selectedComponent === "None"){
          setCurrentUserId(localStorage.getItem('userId') || null)
          setShowInteractiveTimeline(false)
        }else{
          setCurrentUserId(localStorage.getItem('userId') || null)
          setShowInteractiveTimeline(true)
        }
  };

  const handleOpenInteractiveTimeline = () => {
    setCurrentUserId(localStorage.getItem('userId') || null)
    setShowInteractiveTimeline(!showInteractiveTimeline)
  }

  const fetchTimeLineStory = async () => {
    try{
        console.log("fetching timeline story for user:", currentUserId);
        const response = await axios.get('http://127.0.0.1:8000/insta-user/user-story/' + currentUserId);
        if(response.data && response.data.success){                    
            console.log("fetched timeline story:", response.data);
            setUserTimelineStory(response.data.user_story);
        }

    }catch(error){
        console.error('Error fetching timeline data:', error);
    }
}

    const handleOpenTimelineDialog = () => {
      fetchTimeLineStory();
      setOpenTimelineStoryDialog(true);
    };

    const handleCloseTimelineDialog = () => {
      setOpenTimelineStoryDialog(false);
    };

    const handleShowWordGraph = async () => {
      try {
          //const response = await axios.get('http://127.0.0.1:8000/insta-user/user_object_graph');
          //setWordGraphData(response.data);

          const response = {data: {}}
          response.data = testData;
          createWordGraph(response.data);
      } catch (error) {
          console.error('Error fetching word graph data:', error);
      }
    };

    const createWordGraph = async (wordgraph) => {
      try{
       
        const data = convertData(wordgraph);
        console.log('Word Graph Data:', data);
        setWordGraphData(data);
        setShowWordGraph(true);

      }catch(error){
        console.error('Error creating word graph:', error);
      } 
    };
    const calculateMidpoint = (x1, y1, x2, y2) => {
      const midX = (x1 + x2) / 2;
      const midY = (y1 + y2) / 2;
      return { midX, midY };
  };
    const convertData = (data) => {
      const graphNodesRaw = data.graph.nodes;
      const nodes = graphNodesRaw.map(node => {
        
        var nodeColor = '#e18844'
        var nodeRadius = 10;
        if(node.count > 2){
          nodeColor = '#2596be'
          nodeRadius = 30;
        }else if(node.count > 1){
          nodeColor = '#26deb0'
          nodeRadius = 20;
        }else{
          nodeColor = '#e18844'
          nodeRadius = 15;
        }
        
        const nodeResult = {
          x: node.posx * nodeMultiplier, // Scale positions for better visualization
          y: node.posy * nodeMultiplier,
          color: nodeColor,
          id: node.id,
          count: node.count,
          radius: nodeRadius
        }
        return nodeResult;
    });

      const links = data.graph.edges
      .filter(edge => edge.source !== edge.target) // Filter out edges where source.id equals target.id
      .map(edge => {
          const source = graphNodesRaw.find(node => node.id === edge.source);
          const target = graphNodesRaw.find(node => node.id === edge.target);
          const edgeResult = {
              source: {x: source.posx * nodeMultiplier, y: source.posy * nodeMultiplier},
              target: {x: target.posx * nodeMultiplier, y: target.posy * nodeMultiplier},
              dashed:false,
              weight: edge.weight,
 
          };
 
          const { midX, midY } = calculateMidpoint(edgeResult.source.x, edgeResult.source.y, edgeResult.target.x, edgeResult.target.y);
          
          edgeResult.midx = midX;
          edgeResult.midy = midY;
          return edgeResult;
      });

      console.log("links");
      console.log(links);
      return { nodes, links };
    };
    return (
        <>
         <Container disableGutters maxWidth={false} sx={{ mt: 2 }}>
            <Box sx={{ display:'flex', flexDirection: 'row', my: 4, width: '100%', justifyContent: 'center', alignItems: 'center' }}>
            <Box sx={{ display:'flex', flexDirection: 'row', my: 4, width: '100%', justifyContent: 'center', alignItems: 'center' }}>
              <Link href={"https://www.instagram.com/oauth/authorize?enable_fb_login=0&force_authentication=1&client_id=1573243976639384&redirect_uri=https://localhost:3000/insta-redirect&response_type=code&scope=business_basic%2Cbusiness_manage_messages%2Cbusiness_manage_comments%2Cbusiness_content_publish"} 
              target="_blank" rel="noopener" variant="body1">Link Account</Link>                                
              
              <Button variant="contained" color="primary" onClick={handleShowWordGraph} sx={{ mt: 2 }}>
                Show Word Graph
              </Button>
              <Button variant="contained" color="secondary" onClick={handleOpenChat} sx={{ mt: 2, ml: 2 }}>
                        Open Chat
                    </Button>
              <Button variant="contained" color="primary" onClick={handleOpenTimeline} sx={{ mt: 2, ml: 2 }}>
                  {showTimeline ? 'Hide Timeline' : 'Show Timeline'}
              </Button>
              {/* <Button variant="contained" color="primary" onClick={handleOpenInteractiveTimeline} sx={{ mt: 2, ml: 2 }}>
                  {showInteractiveTimeline ? 'Hide Interactive Timeline' : 'Show Interactive Timeline'}
              </Button> */}
                
                  <FormControl variant="outlined" sx={{ mt: 2, ml: 2, minWidth: 120 }}>
                      <InputLabel id="component-select-label">Select Component</InputLabel>
                      <Select
                          labelId="component-select-label"
                          value={timelineSelectedComponent}
                          onChange={handleTimelineSelectedComponentChange}
                          label="Select Component"
                      >
                          <MenuItem value="None">None</MenuItem>
                          <MenuItem value="interactiveTimeline">Interactive Timeline</MenuItem>
                          <MenuItem value="interactiveGraph">Interactive Graph</MenuItem>
                          {/* Add more MenuItem components as needed */}
                      </Select>
                  </FormControl>

                
              
              <Button variant="contained" color="primary" onClick={handleOpenTimelineDialog} sx={{ mt: 2, ml: 2 }}>
                  Timeline Story
              </Button>
            </Box>
              {(openChatDialog || showTimeline) && (
                  <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start', width: '100%', height:'80vh' }}>
                  <Box sx={{ flex: 7, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  {showTimeline && ( <TimelineComponent userId={currentUserId} showTimeline={showTimeline} />)}
                  </Box>
                  <Box sx={{ flex: 3, width: '100%', height:'100%'   }}>
                  {openChatDialog && ( <ChatComponent></ChatComponent>)}
                  </Box>
                  </Box>
              )}
              {showInteractiveTimeline && (
                <Box sx={{ width: '100%', height: '80vh' }}>
                    <InteractiveTimelineComponent userId={currentUserId} showTimeline={showInteractiveTimeline} selectedTimeline={timelineSelectedComponent} />
                </Box>
              )}
              {/* <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start', width: '100%', height:'80vh' }}>
                <Box sx={{ flex: 6, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  {showTimeline && <TimelineComponent userId={currentUserId} showTimeline={showTimeline} />}
                </Box>
                <Box sx={{ flex: 4, width: '100%', height:'100%'   }}>
                  {openChatDialog && ( <ChatComponent></ChatComponent>)}
                </Box>

              </Box> */}

              {showWordGraph && wordGraphData && (
                  <Box  sx={{ mt: 4 }}>
                      <Typography variant="h5">Word Graph</Typography>
                      {/* Render the word graph data here */}
                      {/* <pre>{JSON.stringify(wordGraphData, null, 2)}</pre> */}
                      <Box sx={{ width: '100%', height: '200vh',boxShadow: 3 }}>
                        <svg width="100%" height="100%">
                            {/* <Graph left={500} top={200} graph={wordGraphData} linkComponent={DefaultLink} nodeComponent={DefaultNode} /> */}
                            <Graph
                              left={1000} top={400}
                              graph={wordGraphData}
                              nodeComponent={({ node: { color,id,count,radius } }) =>
                                color ? <><circle r={radius} fill={color}>
                                  
                                </circle>
                                <text fill="white" fontSize={radius/2} textAnchor="middle">{id}</text></>
                                 : <DefaultNode />
                              }
                              
                              linkComponent={({ link: { source, target, dashed, weight, midx, midy } }) => 
                                <>
                                <line
                                  x1={source.x}
                                  y1={source.y}
                                  x2={target.x}
                                  y2={target.y}
                                  strokeWidth={weight*1.5}
                                  stroke="grey"
                                  strokeOpacity={0.6}
                                  strokeDasharray={dashed ? '8,4' : undefined}
                                />
                                {/* <text fill="black" x={midx} y={midy} >{weight}</text> */}
                                </>
                              }
                            />
                            <text></text>
                        </svg>
                      </Box>
                  </Box>
              )}
             
              
            </Box>
          </Container>
          <Dialog open={openTimelineStoryDialog} onClose={handleCloseTimelineDialog} maxWidth="lg" fullWidth>
              <DialogTitle>User Timeline</DialogTitle>
              <DialogContent>
                  {userTimelineStory && (
                    <Typography variant="body1">
                      {userTimelineStory}
                    </Typography>
                  )}
              </DialogContent>
              <DialogActions>
                  <Button onClick={handleCloseTimelineDialog} color="primary">
                      Close
                  </Button>
              </DialogActions>
          </Dialog>

        </>
    )
}

export default InstaPersonaComponent;