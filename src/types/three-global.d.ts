import { Object3DNode } from '@react-three/fiber';
import * as THREE from 'three';

// Extend the global JSX namespace for React Three Fiber
declare global {
  namespace JSX {
    interface IntrinsicElements {
      // Three.js mesh elements
      mesh: Object3DNode<THREE.Mesh, typeof THREE.Mesh>;
      group: Object3DNode<THREE.Group, typeof THREE.Group>;
      points: Object3DNode<THREE.Points, typeof THREE.Points>;
      instancedMesh: Object3DNode<THREE.InstancedMesh, typeof THREE.InstancedMesh>;
      
      // Geometries
      sphereGeometry: Object3DNode<THREE.SphereGeometry, typeof THREE.SphereGeometry>;
      boxGeometry: Object3DNode<THREE.BoxGeometry, typeof THREE.BoxGeometry>;
      bufferGeometry: Object3DNode<THREE.BufferGeometry, typeof THREE.BufferGeometry>;
      coneGeometry: Object3DNode<THREE.ConeGeometry, typeof THREE.ConeGeometry>;
      octahedronGeometry: Object3DNode<THREE.OctahedronGeometry, typeof THREE.OctahedronGeometry>;
      tetrahedronGeometry: Object3DNode<THREE.TetrahedronGeometry, typeof THREE.TetrahedronGeometry>;
      icosahedronGeometry: Object3DNode<THREE.IcosahedronGeometry, typeof THREE.IcosahedronGeometry>;
      ringGeometry: Object3DNode<THREE.RingGeometry, typeof THREE.RingGeometry>;
      torusGeometry: Object3DNode<THREE.TorusGeometry, typeof THREE.TorusGeometry>;
      
      // Materials
      meshBasicMaterial: Object3DNode<THREE.MeshBasicMaterial, typeof THREE.MeshBasicMaterial>;
      meshStandardMaterial: Object3DNode<THREE.MeshStandardMaterial, typeof THREE.MeshStandardMaterial>;
      meshPhysicalMaterial: Object3DNode<THREE.MeshPhysicalMaterial, typeof THREE.MeshPhysicalMaterial>;
      pointsMaterial: Object3DNode<THREE.PointsMaterial, typeof THREE.PointsMaterial>;
      
      // Lights
      ambientLight: Object3DNode<THREE.AmbientLight, typeof THREE.AmbientLight>;
      pointLight: Object3DNode<THREE.PointLight, typeof THREE.PointLight>;
      spotLight: Object3DNode<THREE.SpotLight, typeof THREE.SpotLight>;
      
      // Other elements
      color: Object3DNode<THREE.Color, typeof THREE.Color>;
      fog: Object3DNode<THREE.Fog, typeof THREE.Fog>;
      bufferAttribute: Object3DNode<THREE.BufferAttribute, typeof THREE.BufferAttribute>;
    }
  }
}

export {}; 