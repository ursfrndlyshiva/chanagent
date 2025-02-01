import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography, Box, CircularProgress } from '@mui/material';

function App() {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false); // State to handle loading
  const chatEndRef = useRef(null); // Ref to scroll to the last message

  useEffect(() => {
    const storedChatHistory = localStorage.getItem('chat_history');
    if (storedChatHistory) {
      setChatHistory(JSON.parse(storedChatHistory));
    }
  }, []);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Create a new chat entry with just the user input
    const newUserChat = { user_input: userInput, response_message: '' };

    // Update chat history with user's input immediately
    const updatedChatHistory = [...chatHistory, newUserChat];

    // Save the updated history to localStorage and update state
    localStorage.setItem('chat_history', JSON.stringify(updatedChatHistory));
    setChatHistory(updatedChatHistory);

    // Clear input field
    setUserInput('');

    // Show loader for 1.5 seconds before sending request
    setLoading(true);

    // Simulate a delay for the loader
    setTimeout(async () => {
      try {
        // Send user input to the backend
        const response = await axios.post('http://localhost:5000/api/submit', {
          user_input: userInput,
        });

        // Get the agent's response
        const agentResponse = response.data.message;

        // Update the chat history with the agent's response
        const finalChatHistory = updatedChatHistory.map((chat) =>
          chat.user_input === userInput
            ? { ...chat, response_message: agentResponse }
            : chat
        );

        // Save the final updated chat history
        localStorage.setItem('chat_history', JSON.stringify(finalChatHistory));
        setChatHistory(finalChatHistory);
      } catch (error) {
        console.error('Error submitting input:', error);
        const errorChat = { user_input: userInput, response_message: 'Error submitting input' };
        const finalChatHistory = [...updatedChatHistory, errorChat];
        setChatHistory(finalChatHistory);
        localStorage.setItem('chat_history', JSON.stringify(finalChatHistory));
      } finally {
        // Hide loader after response is received or if there's an error
        setLoading(false);
      }
    }, 1500); // 1.5-second delay
  };

  return (
    <Container maxWidth="md" sx={{ paddingTop: 4 }}>
      <Typography variant="h4" gutterBottom align="center">
        ___ENQUIRY___
      </Typography>
      <Box
        sx={{
          height: '400px',
          overflowY: 'auto',
          marginBottom: 2,
          padding: 2,
          border: '1px solid #ddd',
          borderRadius: 1,
          backgroundColor: '#f9f9f9',
        }}
      >
        {chatHistory.length === 0 ? (
          <Typography variant="body1" align="center">
            No conversation yet.
          </Typography>
        ) : (
          chatHistory.map((chat, index) => (
        <p  >
          
          <Box
                sx={{
                 display:"flex"
                }}
              >
                <Typography variant="body2"  sx={{
                  backgroundColor: '#2df3ee',
                  justifyContent:"flex-end",
                  marginLeft:"auto",
                  padding: 1,
                     borderRadius: 1,
                     maxWidth: '70%',
                     wordBreak: 'break-word', // Agent's messages on the left
                     marginBottom: 1,
                }} align="left">
                {chat.user_input} <strong>: User</strong>
                </Typography>
              </Box>

              {chat.response_message && (
                <Box
                  sx={{
                    display: 'flex',
                   
                  }}
                >
                  <Typography variant="body2" sx={{ backgroundColor: '#e3f2fd',
                    padding: 1,
                    borderRadius: 1,
                    maxWidth: '70%',
                    wordBreak: 'break-word'}} align="left">
                    <strong>Agent:</strong> {chat.response_message || 'Loading...'}
                  </Typography>
                </Box>
              )}

              {/* Loader while waiting for agent response */}
              {!chat.response_message && loading && (
                <Box
                  sx={{
                    backgroundColor: '#e3f2fd',
                    padding: 1,
                    borderRadius: 1,
                    maxWidth: '70%',
                    wordBreak: 'break-word',
                    marginRight: 'auto', // Keep the loader on the left
                    marginBottom: 1,
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  <CircularProgress size={24} sx={{ marginRight: 2 }} />
                  <Typography variant="body2" align="left">
                    <strong>Agent:</strong> Please wait...
                  </Typography>
                </Box>
              )}

            </p>
          ))
        )}
        <div ref={chatEndRef} /> {/* Scroll target */}
      </Box>

      {/* Input form */}
      <form onSubmit={handleSubmit}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <TextField
            label="Enter your message"
            variant="outlined"
            fullWidth
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            required
            sx={{ flex: 1 }}
          />
          <Button variant="contained" color="primary"   sx={{
        borderRadius: '50%',       // Makes the button circular
        padding: '12px',           // Adds some padding to ensure the icon fits well
        minWidth: 'auto',          // Ensures the button doesn't stretch
        width: '70px',             // Button width
        height: '60px',            // Button height
        display: 'flex',
        justifyContent: 'center',  // Centers the icon horizontally
        alignItems: 'center'       // Centers the icon vertically
      }} type="submit">
           SEND
          </Button>
        </Box>
      </form>
    </Container>
  );
}

export default App;
