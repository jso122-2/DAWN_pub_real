import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import TestComponent from './TestComponent.jsx'
import './gloabals.css'

console.log('🚀 DAWN Frontend Starting...')

// Test if React is working
const rootElement = document.getElementById('root')
console.log('Root element found:', rootElement)

if (rootElement) {
  try {
    const root = ReactDOM.createRoot(rootElement)
    console.log('React root created successfully')
    
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    )
    console.log('React app rendered successfully')
  } catch (error) {
    console.error('Error creating React root or rendering:', error)
  }
} else {
  console.error('Root element not found!')
}
