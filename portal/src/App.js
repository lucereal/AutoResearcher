
import './App.css';
import React, { useState } from 'react';
import { Container, createTheme, ThemeProvider, CssBaseline, Box, AppBar, Toolbar, Typography } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainContainer from './Components/MainComponent';
import PreviewLandingPageComponent from './Components/PreviewLandingPageComponent';
import InstaPersonaComponent from './Components/InstaPersonaComponent';
import InstagramRedirectHandler from './Components/InstaRedirectHandler';

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const theme = createTheme({
        palette: {
            mode: darkMode ? 'dark' : 'light',
        },
    });

  return (
    <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <Box sx={{ flexGrow: 1 }}>
                    <AppBar position="fixed" sx={{ bgcolor: 'background.paper', boxShadow: 'none' }}>
                        <Toolbar>
                            <Typography
                                variant="h6"
                                noWrap
                                
                                component="a" href="/"
                                sx={{
                                    mr: 2,
                                    fontFamily: 'monospace',
                                    fontWeight: 700,
                                    letterSpacing: '.3rem',
                                    color: 'primary.main',
                                    textDecoration: 'none'
                                }}
                            >
                                AutoResearcher
                            </Typography>
                            <Box sx={{ flexGrow: 1 }} />
                        
                        </Toolbar>
                    </AppBar>
                </Box>.
                <Container id="foo" sx={{mr:0, ml:0}} maxWidth={false} disableGutters >
                    <Routes>
                        <Route path="/" element={<MainContainer />} />
                        <Route path="/early" element={<PreviewLandingPageComponent />} />
                        <Route path="/insta-persona" element={<InstaPersonaComponent />} />
                        <Route path="/insta-redirect" element={<InstagramRedirectHandler />} /> {/* Add the new route */}
                        {/* <Route path="/input" element={<InputComponent />} />
                     */}
                        {/* <Route path="/about" element={<AboutComponent setShowSettings={setShowSettings} />} /> */}

                        <Route path="/receipt" element={<div><h1>NEW</h1></div>} />
                    </Routes>
                </Container>
            </Router>
        </ThemeProvider>
  );
}

export default App;
