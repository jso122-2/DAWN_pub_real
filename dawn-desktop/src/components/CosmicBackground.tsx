import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export function CosmicBackground() {
  const starsRef = useRef<THREE.Points>(null)
  
  // Create star geometry
  const starsGeometry = useMemo(() => {
    const geometry = new THREE.BufferGeometry()
    const starCount = 150
    const positions = new Float32Array(starCount * 3)
    const sizes = new Float32Array(starCount)
    const colors = new Float32Array(starCount * 3)
    
    for (let i = 0; i < starCount; i++) {
      const i3 = i * 3
      positions[i3] = (Math.random() - 0.5) * 100
      positions[i3 + 1] = (Math.random() - 0.5) * 100
      positions[i3 + 2] = (Math.random() - 0.5) * 100
      
      sizes[i] = Math.random() * 2
      
      colors[i3] = 0.8 + Math.random() * 0.2
      colors[i3 + 1] = 0.8 + Math.random() * 0.2
      colors[i3 + 2] = 1
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1))
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
    
    return geometry
  }, [])

  // Create star material
  const starsMaterial = useMemo(() => {
    return new THREE.PointsMaterial({
      size: 0.1,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      sizeAttenuation: true
    })
  }, [])

  // Animation
  useFrame((state, delta) => {
    if (starsRef.current) {
      // starsRef.current.rotation.y += delta * 0.05
      // starsRef.current.rotation.x += delta * 0.02
    }
  })

  return (
    <points ref={starsRef} geometry={starsGeometry} material={starsMaterial} />
  )
}