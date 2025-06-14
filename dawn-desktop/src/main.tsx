import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { ConfigProvider } from './providers/ConfigProvider'
import { RouterProvider, ConnectionStatus } from './providers/RouterProvider'
import { ErrorBoundary } from './components/core/ErrorBoundary'
import './styles/index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter>
        <ConfigProvider>
          <RouterProvider>
            <ConnectionStatus />
            <App />
          </RouterProvider>
        </ConfigProvider>
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>,
)