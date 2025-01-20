import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Typography } from '@mui/material';
import axios from 'axios';


const InstaRedirectHandler = () => {
    const location = useLocation();
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const fetchInstagramData = async (code) => {
            try {
                console.log(code);
                // ${process.env.REACT_APP_INSTAGRAM_CLIENT_ID}
                const data = {
                    source: 'local',
                    code: code
                }
                const response = await axios.post('http://127.0.0.1:8000/insta-user/get-user', data);
                console.log(response);
                setUserData(response.data);
            } catch (error) {
                console.error('Error fetching Instagram data:', error);
            } finally {
                // setLoading(false);
            }
        };

        const queryParams = new URLSearchParams(location.search);
        const code = queryParams.get('code');
        if (code) {
            console.log('Authorization Code:', code);
            fetchInstagramData(code);
            // You can now use the authorization code to exchange for an access token
        }
    }, [location]);

    return (
        <Container>
            <Typography variant="h4">Instagram Authorization</Typography>
            <Typography variant="body1">Processing your authorization...</Typography>
        </Container>
    );
};

export default InstaRedirectHandler;