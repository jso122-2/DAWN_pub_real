import { useRef, useEffect } from 'react'

export function CosmicBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()

    // Create stars
    const stars: Array<{
      x: number
      y: number
      z: number
      size: number
      opacity: number
      speed: number
    }> = []

    for (let i = 0; i < 150; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        z: Math.random() * 1000,
        size: Math.random() * 2 + 0.5,
        opacity: Math.random() * 0.8 + 0.2,
        speed: Math.random() * 0.5 + 0.1
      })
    }

    // Animation loop
    let animationId: number
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // Draw stars
      stars.forEach(star => {
        const scale = (1000 - star.z) / 1000
        const x = star.x * scale + canvas.width / 2 * (1 - scale)
        const y = star.y * scale + canvas.height / 2 * (1 - scale)
        const size = star.size * scale
        
        ctx.save()
        ctx.globalAlpha = star.opacity * scale
        ctx.fillStyle = `hsl(${200 + Math.random() * 60}, 70%, 80%)`
        ctx.beginPath()
        ctx.arc(x, y, size, 0, Math.PI * 2)
        ctx.fill()
        ctx.restore()
        
        // Move star towards viewer
        star.z -= star.speed
        if (star.z <= 0) {
          star.z = 1000
          star.x = Math.random() * canvas.width
          star.y = Math.random() * canvas.height
        }
      })
      
      animationId = requestAnimationFrame(animate)
    }

    animate()

    // Handle resize
    const handleResize = () => {
      resizeCanvas()
    }
    window.addEventListener('resize', handleResize)

    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 z-0 pointer-events-none"
      style={{
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)'
      }}
    />
  )
}