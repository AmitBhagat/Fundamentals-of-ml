'use client'

import React from 'react'
import { Mafs, Coordinates, Theme } from 'mafs'
import 'mafs/core.css'

interface MafsVisualizerProps {
  children: React.ReactNode
  height?: number
  width?: 'auto' | number
}

export function MafsVisualizer({ children, height = 400 }: MafsVisualizerProps) {
  return (
    <div className="w-full rounded-xl border bg-card shadow-sm overflow-hidden my-6">
      <Mafs height={height} viewBox={{ x: [-5, 5], y: [-5, 5] }}>
        <Coordinates.Cartesian />
        {children}
      </Mafs>
    </div>
  )
}

export { Theme }
