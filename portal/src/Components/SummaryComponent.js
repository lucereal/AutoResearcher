import {Container, Box, Typography, useMediaQuery, AccordionDetails, AccordionActions, Accordion, AccordionSummary,
    TextField, Button, Link, CircularProgress
} from '@mui/material';
import useTheme from '@mui/material/styles/useTheme';
import { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import test_data from '../testdata/test_data.json';
import { spiral } from 'ldrs'

spiral.register()




const SummaryComponent = () => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const [data, setData] = useState(null);
    const [topic, setTopic] = useState('');
    const [loading, setLoading] = useState(false);


    const handleTopicChange = (event) => {
        setTopic(event.target.value);
    };
    const callResearchApi = async () => {
        console.log('Calling API...');
        setLoading(true);

        try {
            const reqData = {
                topic: topic,
                source: 'default_source'
            };
            const response = await axios.post('http://127.0.0.1:8000/gather_data', reqData);
            
            console.log(test_data);
            setData(response.data);
            console.log('API response:', response);
        } catch (error) {
            console.error('Error calling API:', error);
        } finally {
            setLoading(false);

        }
    };

    return (
        <>
            <Container>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
                    <Typography variant="h4">Summary</Typography>
                    <TextField
                        label="Topic"
                        variant="outlined"
                        value={topic}
                        onChange={handleTopicChange}
                        sx={{ mb: 2 }}
                    />
                <Button variant="contained" color="primary" onClick={callResearchApi}>
                    Submit
                </Button>
                

                <Box sx={{ mt: 4, width: '100%' }}> {/* Add margin-top and set width */}
                {loading && <l-spiral size="40" speed="0.9" color="black" ></l-spiral>}

                    {data && data.full_summary && (
                            <ReactMarkdown>{data.full_summary}</ReactMarkdown>
                        )}

                    {/* {data && data.phrase_results.map((topic, index) => (
                    topic.results && topic.results.map((result, idx) => (
                        <Accordion key={idx}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                <Typography variant="h6">{result.title}</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Link href={result.url} target="_blank" rel="noopener" variant="body1">Source</Link>                                
                                <ReactMarkdown>{result.executive_summary}</ReactMarkdown>
                            </AccordionDetails>
                        </Accordion>
                    )) */}
                {/* ))} */}
                </Box>
                </Box>
            </Container>
        </>
    );

  

}

export default SummaryComponent;