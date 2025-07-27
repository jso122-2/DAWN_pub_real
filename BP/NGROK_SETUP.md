# ngrok Setup for DAWN Desktop

This guide explains how to set up ngrok tunnels for the DAWN Desktop application to enable remote access with both HTTP and WebSocket support.

## Prerequisites

1. **ngrok account and installation**
   - Sign up at [ngrok.com](https://ngrok.com)
   - Download and install ngrok
   - Get your authtoken from [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)

2. **Required services**
   - Computer Vision Backend (port 8081)
   - Frontend Development Server (port 5175)
   - Optional: Main DAWN Backend (port 8000)

## Quick Setup

### Step 1: Configure ngrok

1. Edit `ngrok.yml` and replace `YOUR_NGROK_AUTH_TOKEN_HERE` with your actual token:
   ```yaml
   authtoken: your_actual_token_here
   ```

2. Optionally, customize the tunnel names and ports if needed.

### Step 2: Start all services

**Linux/macOS:**
```bash
chmod +x start_ngrok_tunnels.sh
./start_ngrok_tunnels.sh
```

**Windows:**
```cmd
start_ngrok_tunnels.bat
```

### Step 3: Access your tunnels

1. Open the ngrok dashboard: http://localhost:4040
2. Note the public URLs for each tunnel
3. Use these URLs to access your application remotely

## Manual Setup (Alternative)

If you prefer to start services manually:

### 1. Start the CV Backend
```bash
python computer_vision/cv_server.py
```

### 2. Start the Frontend
```bash
cd dawn-desktop
npm run dev
```

### 3. Start ngrok tunnels

**Option A: Using config file**
```bash
ngrok start --all --config ngrok.yml
```

**Option B: Individual tunnels**
```bash
# Terminal 1 - Frontend tunnel
ngrok http 5175 --host-header="localhost:5175"

# Terminal 2 - CV Backend tunnel  
ngrok http 8081 --host-header="localhost:8081"

# Terminal 3 - (Optional) Main backend tunnel
ngrok http 8000 --host-header="localhost:8000"
```

## Understanding the Configuration

### ngrok.yml explained:

```yaml
version: "2"
authtoken: YOUR_NGROK_AUTH_TOKEN_HERE

tunnels:
  frontend:                    # Tunnel name
    proto: http               # Protocol (HTTP/HTTPS)
    addr: 5175               # Local port to tunnel
    host_header: "localhost:5175"  # Preserve host header
    inspect: true            # Enable traffic inspection
    bind_tls: true          # Force HTTPS
    
  cv-backend:
    proto: http
    addr: 8081
    host_header: "localhost:8081"
    inspect: true
    bind_tls: true
```

### Key Configuration Options:

- `host_header`: Preserves the original host header for proper routing
- `inspect: true`: Enables traffic inspection in ngrok dashboard
- `bind_tls: true`: Forces HTTPS connections for security
- `proto: http`: Supports both HTTP and WebSocket over HTTP tunnels

## WebSocket Support

ngrok automatically supports WebSocket connections over HTTP tunnels. The configuration above will handle:

- HTTP requests to your services
- WebSocket connections from the frontend to the CV backend
- Real-time video streaming
- SocketIO communication

## Troubleshooting

### Common Issues:

1. **"ngrok not found"**
   - Install ngrok from https://ngrok.com/download
   - Add ngrok to your system PATH

2. **"tunnel session failed"**
   - Check your authtoken in ngrok.yml
   - Verify your ngrok account has available tunnels

3. **"port already in use"**
   - Stop any existing services on the required ports
   - Check for existing ngrok processes: `ps aux | grep ngrok`

4. **WebSocket connection fails**
   - Ensure you're using the ngrok HTTPS URL (not HTTP)
   - Check that `host_header` is set correctly
   - Verify the CV backend is running on port 8081

### Debugging:

1. **Check ngrok dashboard**: http://localhost:4040
   - View live traffic
   - See error messages
   - Monitor WebSocket connections

2. **Check service logs**:
   - CV Backend: Look for startup messages
   - Frontend: Check browser console for errors
   - ngrok: Watch for connection errors

3. **Test connections**:
   ```bash
   # Test CV backend
   curl http://localhost:8081/health
   
   # Test through ngrok (replace with your URL)
   curl https://abc123.ngrok.io/health
   ```

## Security Considerations

1. **HTTPS enforcement**: The configuration forces HTTPS for security
2. **Tunnel protection**: Consider using ngrok's password protection for sensitive environments
3. **Firewall**: ngrok bypasses local firewalls - be mindful of exposed endpoints

## Advanced Configuration

### Custom domains (ngrok Pro):
```yaml
tunnels:
  frontend:
    proto: http
    addr: 5175
    hostname: dawn-frontend.your-domain.com
```

### Basic authentication:
```yaml
tunnels:
  frontend:
    proto: http
    addr: 5175
    auth: "username:password"
```

### IP restrictions:
```yaml
tunnels:
  frontend:
    proto: http
    addr: 5175
    cidr_allow:
      - "192.168.1.0/24"
```

## Monitoring

- **ngrok Dashboard**: http://localhost:4040
- **CV Backend Health**: http://localhost:8081/health
- **Frontend**: http://localhost:5175

All services include health checks and status endpoints for monitoring. 