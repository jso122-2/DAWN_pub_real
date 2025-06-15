import React from 'react';

// Override the @react-three/drei types to fix the ReactNode incompatibility
declare module '@react-three/drei' {
  export interface OrbitControlsProps {
    enableZoom?: boolean;
    enablePan?: boolean;
    enableRotate?: boolean;
    autoRotate?: boolean;
    autoRotateSpeed?: number;
    minDistance?: number;
    maxDistance?: number;
    minPolarAngle?: number;
    maxPolarAngle?: number;
    [key: string]: any;
  }
  
  export interface TextProps {
    position?: [number, number, number];
    fontSize?: number;
    color?: string;
    anchorX?: string;
    anchorY?: string;
    textAlign?: string;
    children?: React.ReactNode;
    [key: string]: any;
  }
  
  export interface StarsProps {
    radius?: number;
    depth?: number;
    count?: number;
    factor?: number;
    fade?: boolean;
    [key: string]: any;
  }
  
  export interface PerspectiveCameraProps {
    makeDefault?: boolean;
    position?: [number, number, number];
    fov?: number;
    aspect?: number;
    near?: number;
    far?: number;
    [key: string]: any;
  }
  
  export interface BoxProps {
    args?: [number, number, number];
    [key: string]: any;
  }
  
  export interface SphereProps {
    args?: [number, number?, number?];
    position?: [number, number, number];
    [key: string]: any;
  }
  
  export interface LineProps {
    points?: any[];
    color?: string;
    lineWidth?: number;
    [key: string]: any;
  }
  
  export const OrbitControls: React.FC<OrbitControlsProps>;
  export const Text: React.FC<TextProps>;
  export const Stars: React.FC<StarsProps>;
  export const PerspectiveCamera: React.FC<PerspectiveCameraProps>;
  export const Box: React.FC<BoxProps>;
  export const Sphere: React.FC<SphereProps>;
  export const Line: React.FC<LineProps>;
}

export {}; 