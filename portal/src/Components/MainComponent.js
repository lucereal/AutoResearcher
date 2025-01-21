import {Button, Container, Box, Typography, useMediaQuery} from '@mui/material';
import useTheme from '@mui/material/styles/useTheme';
import SummaryComponent from './SummaryComponent';
import { useState,useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const MainContainer = () => {
    const theme = useTheme();
    const navigate = useNavigate();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const [showSummaryComponent, setShowSummaryComponent] = useState(false);

    const handleButtonClick = () => {
       navigate('/insta-persona');
        
    };

    useEffect(() => {
        injectFacebookSDK();
    }, []);


    const statusChangeCallback = async (response) => {
        console.log('Facebook login status:', response);
        if(response.status === 'connected') {
            console.log('Logged in and authenticated');
            // Logged into your webpage and Facebook.
            const data = {
                source: 'local',
                code: response.authResponse.accessToken
            }
            console.log("data: ", data);
            const getUserResponse = await axios.post('http://127.0.0.1:8000/insta-user/get-user-fb', data);
            console.log(getUserResponse);
        }
        // Handle the response here
    };

    const checkLoginState = async () => {
        if (window.FB) {
            window.FB.getLoginStatus(function(response) {
                statusChangeCallback(response);
            });
        } else {
            console.error('Facebook SDK not loaded yet.');
        }
    };

    const injectFacebookSDK = () => {

        window.checkLoginState = function (){
            checkLoginState();
        }
        window.fbAsyncInit = function() {
    
            FB.init({
                appId      : '1125867555747483',
                cookie     : true,
                xfbml      : true,
                version    : 'v21.0'
            });
          
            FB.AppEvents.logPageView();   

            // Check login status
            FB.getLoginStatus(function(response) {
                statusChangeCallback(response);
            });

            // FB.XFBML.parse();
        };

        (function(d, s, id){
            console.log("d:", d);
            console.log("s:", s);
            console.log("id:", id);
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) {return;}
            js = d.createElement(s); js.id = id;
            js.src = "https://connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
    };

    return (
        <>
        <Container sx={{ mt: 8 }}>
            <Button variant="contained" color="primary" onClick={handleButtonClick}>
                Insta Persona
            </Button>

            <div
            dangerouslySetInnerHTML={{
                __html: `<fb:login-button scope="public_profile,email" onlogin="checkLoginState();"></fb:login-button>`
            }}
            />

        </Container>
        </>
    )
}

export default MainContainer;