import React from 'react'

export const metadata = { title: '{{PROJECT}}' }

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
