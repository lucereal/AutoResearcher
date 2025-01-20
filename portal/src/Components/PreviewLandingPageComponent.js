import React, { useState } from 'react';
import { Box, Typography, Container, TextField, Button } from '@mui/material';


const PreviewLandingPageComponent = () => {
    const [email, setEmail] = useState('');

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
      };

      const handleSubmit = (event) => {
        event.preventDefault();
        // Handle form submission, e.g., send email to backend or a service
        console.log('Email submitted:', email);
      };

    return (
        <>
         <Container sx={{ mt: 8 }}>
            <Box sx={{ my: 4 }}>
              <Typography variant="h4" component="h1" gutterBottom>
                Welcome to CheckMates
              </Typography>
              <Typography variant="body1" paragraph>
                Here is a brief summary or video about the purpose of the application.
              </Typography>
              <iframe
                width="560"
                height="315"
                src="https://www.youtube.com/embed/YYC8KlT4yNE"
                title="YouTube video player"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4 }}>
                <TextField
                  label="Email"
                  variant="outlined"
                  fullWidth
                  value={email}
                  onChange={handleEmailChange}
                  required
                />
                <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
                  Sign Up for Early Access
                </Button>
              </Box>
            </Box>
          </Container>
        </>
    )
}

export default PreviewLandingPageComponent;