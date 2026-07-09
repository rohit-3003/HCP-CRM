import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../services/api';

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ message, sessionId }) => {
    const response = await api.post('/chat', { message, session_id: sessionId });
    return response.data;
  }
);

const initialState = {
  messages: [{ id: 'init', type: 'ai', text: 'Hello! I am your AI CRM Assistant. How can I help you log an interaction today?' }],
  isLoading: false,
  aiInsights: {
    summary: '',
    sentiment: '',
    missingFields: [],
    confidenceScores: {},
    entities: {}
  },
  executionSteps: [],
  sessionId: 'session_' + Math.random().toString(36).substr(2, 9),
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addUserMessage: (state, action) => {
      state.messages.push({
        id: Date.now().toString(),
        type: 'user',
        text: action.payload
      });
    },
    clearChat: (state) => {
      state.messages = initialState.messages;
      state.aiInsights = initialState.aiInsights;
      state.executionSteps = [];
      state.sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.isLoading = true;
        state.executionSteps = ['Analyzing intent...'];
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        state.messages.push({
          id: Date.now().toString(),
          type: 'ai',
          text: action.payload.response || "I've processed your request."
        });
        
        // Update insights
        state.aiInsights.summary = action.payload.entities?.summary || state.aiInsights.summary;
        state.aiInsights.sentiment = action.payload.sentiment || state.aiInsights.sentiment;
        state.aiInsights.missingFields = action.payload.missing_fields || [];
        state.aiInsights.confidenceScores = action.payload.confidence_scores || {};
        state.aiInsights.entities = action.payload.entities || {};
        
        state.executionSteps = action.payload.execution_steps || [];
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.messages.push({
          id: Date.now().toString(),
          type: 'error',
          text: 'Sorry, there was an error processing your request.'
        });
        state.executionSteps.push("Error connecting to server.");
      });
  },
});

export const { addUserMessage, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
