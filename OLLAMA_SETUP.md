# Ollama Setup Guide for SJIS Chatbot

## What is Ollama?

Ollama is a free, open-source tool that lets you run large language models (LLMs) locally on your computer. It's perfect for the school chatbot because:

- ✅ **100% Free** - No API costs or subscriptions
- 🔒 **Privacy** - All data stays on your server
- ⚡ **Fast** - Runs locally without internet dependency
- 🎯 **Easy** - Simple installation and management

## Installation

### macOS

```bash
# Install Ollama
brew install ollama

# Or download from https://ollama.ai
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows

Download the installer from [https://ollama.com/download](https://ollama.com/download)

## Quick Start

### 1. Start Ollama Service

```bash
# Start Ollama (runs in background)
ollama serve
```

### 2. Pull a Model

The chatbot is configured to use `llama3.2:3b` (recommended for schools - fast and efficient):

```bash
# Download the model (one-time, ~2GB)
ollama pull llama3.2:3b
```

**Other model options:**
- `llama3.2:1b` - Smallest, fastest (good for low-resource servers)
- `llama3.2:3b` - ⭐ **Recommended** - Best balance of speed/quality
- `mistral` - Alternative, very good quality
- `phi` - Microsoft's model, compact and fast

### 3. Test Ollama

```bash
# Test in terminal
ollama run llama3.2:3b "Hello, how are you?"
```

### 4. Verify Integration

The chatbot will automatically detect and use Ollama if it's running. Check the Django logs:

```bash
cd "/Volumes/Drive A/SJIS/sjis/28 NOV 2025/sjis-website"
python3 manage.py runserver
```

Look for: `Successfully connected to Ollama. Using model: llama3.2:3b`

## Usage Notes

### System Requirements

- **RAM**: Minimum 4GB, 8GB+ recommended
- **Storage**: 2-4GB per model
- **CPU**: Any modern processor (GPU optional but faster)

### Automatic Fallback

The chatbot is smart:
- **If Ollama is running** → Uses AI-generated responses
- **If Ollama is not available** → Uses rule-based responses (still works!)

This means your chatbot works even if Ollama isn't installed yet.

### Performance Tips

1. **Keep Ollama running** - Add to startup scripts:
   ```bash
   # macOS/Linux - add to ~/.bashrc or ~/.zshrc
   ollama serve &
   ```

2. **Use smaller models** for faster responses:
   ```bash
   ollama pull llama3.2:1b
   ```
   
   Then update `chatbot/ollama_service.py` line 20:
   ```python
   def __init__(self, model='llama3.2:1b'):
   ```

3. **Monitor resource usage**:
   ```bash
   # Check if Ollama is running
   ps aux | grep ollama
   ```

## Common Issues

### Issue: "Ollama not running"

**Solution:**
```bash
# Start Ollama
ollama serve
```

### Issue: "Model not found"

**Solution:**
```bash
# Pull the model
ollama pull llama3.2:3b
```

### Issue: "Out of memory"

**Solution:**
- Use a smaller model: `ollama pull llama3.2:1b`
- Close other applications
- Increase server RAM

### Issue: Chatbot gives rule-based responses

**Check:**
1. Is Ollama running? `ps aux | grep ollama`
2. Is the model downloaded? `ollama list`
3. Check Django logs for errors

## Changing Models

To use a different model, edit `/chatbot/ollama_service.py`:

```python
def __init__(self, model='mistral'):  # Change here
    """
    Initialize Ollama service.
    ...
```

Then pull the new model:
```bash
ollama pull mistral
```

## Production Deployment

For production on your school server:

1. **Install Ollama** on the server
2. **Set up auto-start**:
   ```bash
   # Create systemd service (Linux)
   sudo nano /etc/systemd/system/ollama.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Ollama Service
   After=network.target
   
   [Service]
   ExecStart=/usr/local/bin/ollama serve
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable:
   ```bash
   sudo systemctl enable ollama
   sudo systemctl start ollama
   ```

3. **Pull your chosen model**
4. **Restart Django**

## Testing the Chatbot

Once Ollama is running:

1. Open your website: `http://127.0.0.1:8000/`
2. Click the chat widget (💬 bottom-right)
3. Ask: "What is the school address?"
4. You should get a natural, AI-generated response!

## Need Help?

- Ollama Documentation: https://ollama.ai/docs
- Model Library: https://ollama.ai/library
- GitHub Issues: https://github.com/ollama/ollama/issues

---

**Note:** The chatbot works perfectly fine without Ollama using rule-based responses. Ollama just makes the responses more natural and conversational!
