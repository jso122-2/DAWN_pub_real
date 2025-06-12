import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Points, PointMaterial } from '@react-three/drei'
import * as THREE from 'three'

export function CosmicBackground() {
  const ref = useRef<THREE.Points>(null)
  
  // Generate random star positions
  const positions = new Float32Array(5000 * 3)
  for (let i = 0; i < 5000; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 100
    positions[i * 3 + 1] = (Math.random() - 0.5) * 100
    positions[i * 3 + 2] = (Math.random() - 0.5) * 100
  }

  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.x = state.clock.elapsedTime * 0.05
      ref.current.rotation.y = state.clock.elapsedTime * 0.075
    }
  })

  return (
    <>
      <color attach="background" args={['#000000']} />
      <fog attach="fog" args={['#000000', 1, 100]} />
      
      <Points ref={ref} positions={positions} stride={3}>
        <PointMaterial
          transparent
          color="#8b5cf6"
          size={0.1}
          sizeAttenuation={true}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </Points>
      
      <ambientLight intensity={0.1} />
      <pointLight position={[10, 10, 10]} intensity={0.5} color="#8b5cf6" />
    </>
  )
}