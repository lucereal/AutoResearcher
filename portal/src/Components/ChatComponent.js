import React, { useState, useEffect, useRef } from 'react';
import {Box, Typography, TextField, Button, Avatar, TextareaAutosize,
   IconButton, CircularProgress, FormControl, InputLabel, Select, MenuItem
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import AddIcon from '@mui/icons-material/Add';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import TimelineComponent from './TimelineComponent';
import { PhotoCamera, Send, Clear } from '@mui/icons-material';

const ChatComponent = () => {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [userId, setUserId] = useState('');
    const [openChat, setOpenChat] = useState(false);
    const [chatName, setChatName] = useState('new chat'); // State variable to store the chat name
    const [olderChats, setOlderChats] = useState({}); // State variable to store older chats
    const [loading, setLoading] = useState(true);
    const messageEndRef = useRef(null); // Reference to the end of the message area
    const [uploadedImages, setUploadedImages] = useState([]); // State to store uploaded images
    const [uploadedImagesFile, setUploadedImagesFile] = useState([]); // State to store uploaded images

    useEffect(() => {
        
        
        let savedUserId = localStorage.getItem('userId');
        if (!savedUserId) {
            savedUserId = uuidv4();
            localStorage.setItem('userId', savedUserId);

            console.log('created new user id: ' + savedUserId);
        }else {
            const chatData = JSON.parse(localStorage.getItem('chatData')) || {};
            const savedChatName = chatData[savedUserId]?.chatName || 'new chat';
            setChatName(savedChatName);
            console.log('loaded chat name:', savedChatName);
        }

        console.log('userId: ' + savedUserId);
        console.log('chat name: ' + chatName);
        // console.log('User ID:', savedUserId);
        setUserId(savedUserId);

        getUserChatHistory(savedUserId);
    }, []);

    useEffect(() => {
        // Load older chats from local storage
        const chatData = JSON.parse(localStorage.getItem('chatData')) || {};
        setOlderChats(Object.entries(chatData));
        console.log('loaded older chats:', chatData);
        setLoading(false);

        Object.entries(olderChats).map(([id, chatData]) => (
            
            console.log('id:', id, 'chatData:', chatData[1].chatName, 'userId:', chatData[0])
        ))

    }, []);

    useEffect(() => {
        // Scroll to the bottom of the message area when messages are updated
        if (messageEndRef.current) {
            messageEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    const handleNewChat = () => {
        const newUserId = uuidv4();
        localStorage.setItem('userId', newUserId);


        setUserId(newUserId);
        localStorage.setItem('userId', newUserId);

        setChatName('new chat');
        setMessages([]);
        saveChatData(newUserId, 'new chat');
    };

    const handleDeleteImage = (index) => {
        setUploadedImages(prevImages => prevImages.filter((_, i) => i !== index));
    };

    const getUserChatHistory = async (userId) => {

        try{
            const response = await axios.get('http://127.0.0.1:8000/insta-user/chat-history/' + userId);
            const chatHistory = response.data;
            const chatMessages = chatHistory
                .filter(chat => (chat.role === 'assistant' || chat.role === 'user') && chat.content !== null)
                .map(chat => ({ text: chat.content, isUser: chat.role === 'user' }));            
            setMessages(chatMessages);
        }catch(error){
            console.error('Error fetching chat data:', error);
        }
    }

    
    const handleOlderChatSelect = (event) => {
        console.log('in handleOlderChatSelect');
        console.log(event.target.value);
        const [selectedUserId, selectedChatName] = event.target.value.split(':');
        setUserId(selectedUserId);
        localStorage.setItem('userId', selectedUserId);
        getUserChatHistory(selectedUserId);
        setChatName(selectedChatName);
        console.log('selectedUserId:', selectedUserId, 'selectedChatName:', selectedChatName);
        const chatData = JSON.parse(localStorage.getItem('chatData')) || {};
        setOlderChats(Object.entries(chatData));
        
    };


    const handleSendMessage = async () => {
        console.log('chat name in handleSendMessage: ' + chatName);
        if (message.trim() !== '') {

            try {

                console.log(message)
                setMessages(prevMessages => [...prevMessages, { text: message, isUser: true }]);
                console.log('messages', messages);

                setMessage('');

                
                const reqData = {
                    user_id: userId,
                    user_message: message
                };

                console.log(reqData);
                // const response = await axios.post('http://127.0.0.1:8000/insta-user/chat-persona', reqData);
                const response = await axios.post('http://127.0.0.1:8000/insta-user/chat-timeline', reqData);
                
                console.log(response);

                setMessages(prevMessages => [...prevMessages, { text: response.data.response, isUser: false }]);


                console.log('messages', messages);
            } catch (error) {
                console.error('Error fetching chat data:', error);
            }
            

        }
    };

    const handleSendMessageWithImage = async () => {
        console.log('chat name in handleSendMessage: ' + chatName);
        if (message.trim() !== '') {
            try {
                setMessages(prevMessages => [...prevMessages, { text: message, isUser: true }]);
                setMessage('');
                const formData = new FormData();
                formData.append('user_id', userId);
                formData.append('user_message', message);
                    
                uploadedImagesFile.forEach((image, index) => {
                    formData.append('images', image);
                });
                setUploadedImages([]);
                const response = await axios.post('http://127.0.0.1:8000/insta-user/chat-timeline-images', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
                
                console.log(response);
                setMessages(prevMessages => [...prevMessages, { text: response.data.response, isUser: false }]);
                console.log('messages', messages);
            } catch (error) {
                console.error('Error fetching chat data:', error);
            }
            

        }
    };

    const handleSend = async () => {
        if(uploadedImages.length > 0){
            console.log('sending message with images')
            handleSendMessageWithImage();
        }else{
            console.log('sending message')
            handleSendMessage();
        }
    }

    const saveChatData = (userId, chatName) => {
        const chatData = JSON.parse(localStorage.getItem('chatData')) || {};
        chatData[userId] = { chatName };
        localStorage.setItem('chatData', JSON.stringify(chatData));
    };

    const handleChatNameChange = (event) => {
        const newChatName = event.target.value;
        setChatName(newChatName);
        saveChatData(userId, newChatName);
    };
    
    const handleUploadPicture = (event) => {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            setUploadedImagesFile(prevImages => [...prevImages, file]);

            const reader = new FileReader();
            reader.onloadend = () => {
                setUploadedImages(prevImages => [...prevImages, reader.result]);
            };
            reader.readAsDataURL(file);
        }
    };
    
    if (loading) {
        return <CircularProgress />;
    }
    return (
        <>
        
       <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', px:2 }}>
                <TextField
                    autoFocus
                    margin="dense"
                    label="Chat Name"
                    type="text"
                    fullWidth
                    placeholder="new chat"
                    value={chatName}
                    onChange={handleChatNameChange}
                    sx={{my:0, mb:1, width: '50%' }}
                />
                <FormControl sx={{ width: '30%', mb:1, ml:1 }}>
                    <InputLabel id="older-chats-label">Chats</InputLabel>
                    <Select
                        labelId="older-chats-label"
                        value={''}
                        label="Chats"
                        onChange={handleOlderChatSelect}
                    >
                        {Object.entries(olderChats).map(([id, chatData]) => {   
                            if(chatData[0] !== userId){
                                return (
                                    <MenuItem key={id} value={`${chatData[0]}:${chatData[1].chatName}`}>
                                    {chatData[1].chatName}
                                    </MenuItem>
                                );
                            }
                            return null; 
                        })}
                    </Select>
                </FormControl>
                <IconButton aria-label="new chat" onClick={handleNewChat} sx={{ ml: 2 }}>
                    <AddIcon />
                </IconButton>
            </Box>
            <Box id="chat-window" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', height: '100%' }}>
                <Box id="message-area" sx={{ flexGrow: 1, overflowY: 'auto', width: '100%' }}>
                    {messages.map((msg, index) => (
                        <Box key={index} sx={{ py: 2, display: 'flex', justifyContent: msg.isUser ? 'flex-end' : 'flex-start' }}>
                            {!msg.isUser && (
                                <Avatar sx={{ bgcolor: 'grey.300', mr: 1 }}>
                                    <PersonIcon />
                                </Avatar>
                            )}
                            <Typography
                                variant="body1"
                                sx={{
                                    bgcolor: msg.isUser ? 'primary.main' : 'grey.300',
                                    color: msg.isUser ? 'white' : 'black',
                                    p: 1,
                                    borderRadius: 1,
                                    maxWidth: '70%',
                                }}
                            >
                                {msg.text}
                            </Typography>
                            {msg.isUser && (
                                <Avatar sx={{ bgcolor: 'primary.main', ml: 1 }}>
                                    <PersonIcon />
                                </Avatar>
                            )}
                        </Box>
                    ))}
                    <div ref={messageEndRef} />
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', p: 2, borderTop: '1px solid #ccc', width: '100%' }}>
                    <TextField
                        multiline
                        maxRows={5}
                        fullWidth
                        placeholder="Type your message..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyPress={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                        sx={{ flexGrow: 1, mr: 2 }}
                    />
                    
            
                    <IconButton color="primary" aria-label="upload picture" onClick={handleSend} component="span">
                        <Send />
                    </IconButton>
                    <input
                        accept="image/*"
                        style={{ display: 'none' }}
                        id="icon-button-file"
                        type="file"
                        onChange={handleUploadPicture}
                    />
                    <label htmlFor="icon-button-file">
                        <IconButton color="primary" aria-label="upload picture" component="span">
                            <PhotoCamera />
                        </IconButton>
                    </label>
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', p: 2, width: '100%' }}>
                    {uploadedImages.map((image, index) => (
                        <Box key={index} sx={{ position: 'relative', display: 'inline-block', m: 1 }}>
                            <img src={image} alt={`uploaded-${index}`} style={{ maxWidth: '150px', maxHeight: '150px', borderRadius: '4px' }} />
                            <IconButton
                                size="small"
                                sx={{ position: 'absolute', top: 0, right: 0, bgcolor: 'rgba(255, 255, 255, 0.7)' }}
                                onClick={() => handleDeleteImage(index)}
                            >
                                <Clear fontSize="small" />
                            </IconButton>
                        </Box>
                    ))}
                </Box>
            </Box>
        </Box>
        </>
    )
}

export default ChatComponent;