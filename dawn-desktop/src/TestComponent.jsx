import React from 'react'

const TestComponent = () => {
  return (
    <div style={{ 
      padding: '20px', 
      backgroundColor: '#1f2937', 
      color: 'white', 
      minHeight: '100vh',
      fontFamily: 'monospace' 
    }}>
      <h1>🧠 DAWN Test Component</h1>
      <p>If you can see this, React is working!</p>
      <div style={{ 
        backgroundColor: '#374151', 
        padding: '10px', 
        marginTop: '20px',
        borderRadius: '8px'
      }}>
        <h3>Debug Info:</h3>
        <p>React Version: {React.version}</p>
        <p>Timestamp: {new Date().toLocaleString()}</p>
      </div>
    </div>
  )
}

export default TestComponent 