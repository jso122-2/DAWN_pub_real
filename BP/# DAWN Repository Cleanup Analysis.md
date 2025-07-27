# DAWN Repository Cleanup Analysis

## 🟢 KEEP - Core Backend Components

### Python Consciousness Engine
```
backend/
├── main.py                  # ✅ KEEP - Core consciousness engine with tick loop
├── start_api_fixed.py       # ✅ KEEP - FastAPI server for WebSocket/API
├── requirements.txt         # ✅ KEEP - Python dependencies
└── config/                  # ✅ KEEP - Configuration files
```

### WebSocket & API Logic
- Tick loop system sending SCUP, entropy, mood signals
- WebSocket connection handlers
- API endpoints for frontend communication
- Any existing data models/schemas

### Python Process Scripts
- Any .py files that are actual consciousness modules
- Visual executables that do real processing
- Utility scripts that support the main engine

## 🔴 CUT - Old Frontend Components

### Remove ALL Glass Morphism UI
```
frontend/src/
├── components/              # ❌ REMOVE ALL
│   ├── ModuleContainer/    # Glass effects, breathing animations
│   ├── StarField/          # Decorative background
│   ├── ProcessModule/      # Old UI components
│   └── *                   # All other old components
├── styles/                 # ❌ REMOVE ALL
├── assets/                 # ❌ REMOVE ALL
├── contexts/              # ❌ REMOVE (rebuild minimal)
├── hooks/                 # ❌ REMOVE (rebuild as needed)
└── utils/                 # ❌ REVIEW (keep only essentials)
```

## 🟡 REVIEW & REFACTOR

### WebSocket Manager
- **Keep**: Core connection logic
- **Refactor**: Simplify to minimal terminal-style status
- **Remove**: Any UI-specific formatting

### Module Registry
- **Keep**: The concept and structure
- **Refactor**: From floating modules to terminal windows
- **Remove**: Animation logic, positioning system

### Data Types/Interfaces
```typescript
// KEEP these core interfaces
interface TickData {
  tick_number: number;
  scup: number;
  entropy: number;
  mood: string;
}

interface PythonProcess {
  script: string;
  status: 'running' | 'completed' | 'error';
  output: any;
}

// REMOVE UI-specific types
type ModuleCategory = 'neural' | 'quantum' | 'chaos' // etc
```

## 📁 New Clean Structure

```
DAWN_pub_real/
├── backend/
│   ├── main.py                    # Core consciousness engine
│   ├── start_api_fixed.py         # API server
│   ├── modules/                   # Python process modules
│   │   ├── __init__.py
│   │   ├── neural_module.py
│   │   ├── quantum_module.py
│   │   └── chaos_module.py
│   ├── utils/                     # Backend utilities
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx              # Entry point
│   │   ├── App.tsx               # Main app with terminal UI
│   │   ├── components/           # New minimal components
│   │   │   ├── Terminal.tsx     # CLI interface
│   │   │   ├── DataGrid.tsx     # Swiss grid data display
│   │   │   ├── ModuleView.tsx   # Single module display
│   │   │   └── StatusBar.tsx    # Connection status
│   │   ├── services/            # Clean service layer
│   │   │   ├── websocket.ts     # WebSocket manager
│   │   │   └── api.ts           # API calls
│   │   ├── types/               # TypeScript interfaces
│   │   │   └── index.ts         # Core data types only
│   │   └── styles/              # Minimal styles
│   │       ├── global.css       # Base styles
│   │       └── terminal.css     # Terminal theme
│   │
│   ├── package.json             # Minimal dependencies
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── docs/                        # Keep if useful
├── scripts/                     # Deployment/utility scripts
├── .gitignore
└── README.md

```

## 🧹 Cleanup Commands

```bash
# Backend cleanup
cd backend/
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete
find . -name ".DS_Store" -delete

# Frontend complete removal
cd frontend/src/
rm -rf components/ styles/ assets/ contexts/ hooks/
rm -rf utils/* # Then selectively restore needed files

# Clean dependencies
cd frontend/
rm -rf node_modules package-lock.json
# Then reinstall with minimal package.json

# Git cleanup
git rm -r --cached node_modules/
git rm -r --cached .DS_Store
git rm -r --cached *.pyc
```

## 🎯 Priority Actions

1. **Immediate**: Remove all glass morphism UI components
2. **Next**: Audit Python modules - keep only active ones
3. **Then**: Rebuild minimal WebSocket connection
4. **Finally**: Create new terminal-based UI components

## 💡 Key Principles

- **Backend**: Keep ALL core logic, just organize better
- **Frontend**: Complete rewrite with minimal dependencies
- **Data Flow**: Preserve existing WebSocket/API structure
- **Modules**: Keep the concept, change the presentation
- **Utils**: Only keep what's actively used

## 🚀 Migration Strategy

1. Create `frontend_old/` backup directory
2. Move current frontend there temporarily
3. Start fresh with new minimal structure
4. Port ONLY the essential connection logic
5. Delete backup once new UI is working