import React, { ReactNode } from "react";

interface BreathingPanelProps {
  children: ReactNode;
  className?: string;
  intensity?: "subtle" | "normal" | "strong";
}

export const BreathingPanel = ({ children, className = "", intensity = "normal" }: BreathingPanelProps) => {
  const intensityClasses: Record<"subtle" | "normal" | "strong", string> = {
    subtle: "animate-breathe opacity-90",
    normal: "animate-breathe",
    strong: "animate-breathe scale-105"
  };
  
  return (
    <div className={`${intensityClasses[intensity]} ${className}`}>
      {children}
    </div>
  );
}; 