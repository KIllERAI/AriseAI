# AriseAI GUI - User Testing Guide

## Quick Start

### 1. Start the Server
From the workspace root:
```powershell
cd c:\Users\Ayan\AriseAI\backend
..\venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

### 2. Open the GUI
- Navigate to: **http://localhost:8000/**

## Features

✅ **Real-time Chat** - Type messages and get instant responses
✅ **Conversation Persistence** - Conversations are saved and continued
✅ **Message Metadata** - See memory load count and message IDs
✅ **User Tracking** - Automatic user ID management via localStorage
✅ **Loading States** - Visual feedback while waiting for responses
✅ **Error Handling** - Clear error messages if requests fail
✅ **Mobile Responsive** - Works on desktop and mobile browsers
✅ **Keyboard Support** - Press Enter to send messages

## How It Works

1. **Enter a message** in the text input box
2. **Click Send** or press **Enter**
3. The message appears on the right (user message)
4. The AI response appears on the left (AI message)
5. Metadata shows:
   - Memory items loaded from previous conversations
   - Unique message ID for tracking

## Data Persistence

- **User ID**: Stored in browser localStorage (persists across sessions)
- **Conversation ID**: Automatically linked to the current conversation
- **Messages**: All messages saved to the database (backend)
- **Memory**: Previous messages retrieved on each new request

## Testing Checklist

- [ ] Server starts without errors
- [ ] GUI loads at http://localhost:8000/
- [ ] Can type and send messages
- [ ] AI responds with text from LLM service
- [ ] Metadata displays correctly
- [ ] Send multiple messages to same user
- [ ] Refresh browser - conversation history persists
- [ ] Open in new browser tab - same user continues same conversation
- [ ] Check database: `backend/arise.db` grows with new messages

## Browser Compatibility

✅ Chrome/Chromium  
✅ Firefox  
✅ Safari  
✅ Edge  

## Troubleshooting

**"Connection Error: fetch failed"**
- Server not running? Start it with the command above
- Port 8000 blocked? Change `--port 8000` to another port

**"No response received"**
- Check LLM service is running
- Check backend logs for errors

**Messages not persisting**
- Check browser console for errors (F12)
- Verify database file exists: `backend/arise.db`
- Check database hasn't hit storage limits

## Next Steps

Once testing is complete:
1. Add voice input (Whisper integration - Phase 2)
2. Add text-to-speech output (Phase 2)
3. Implement smart memory extraction (Phase 3)
4. Add personality system (Phase 4)
5. Add scheduling capabilities (Phase 5)
