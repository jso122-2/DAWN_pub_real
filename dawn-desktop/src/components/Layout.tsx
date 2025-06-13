export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative z-10">
      {/* Don't add backgrounds here - App.tsx handles it */}
      {children}
    </div>
  )
} 