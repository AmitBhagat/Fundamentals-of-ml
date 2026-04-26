'use client'

import React, { useEffect, useRef } from 'react'
import JXG from 'jsxgraph'

interface JSXGraphProps {
  id: string
  initAttributes?: any
  boardAttributes?: any
  render: (board: JXG.Board) => void
  style?: React.CSSProperties
}

export function JSXGraphVisualizer({ id, render, style, boardAttributes = {} }: JSXGraphProps) {
  const boardRef = useRef<JXG.Board | null>(null)

  useEffect(() => {
    // Clean up previous board if any
    if (boardRef.current) {
      JXG.JSXGraph.freeBoard(boardRef.current)
    }

    const board = JXG.JSXGraph.initBoard(id, {
      boundingbox: [-5, 5, 5, -5],
      axis: true,
      showCopyright: false,
      ...boardAttributes,
    })

    render(board)
    boardRef.current = board

    return () => {
      if (boardRef.current) {
        JXG.JSXGraph.freeBoard(boardRef.current)
      }
    }
  }, [id, render, boardAttributes])

  return (
    <div 
      id={id} 
      className="jxgbox w-full aspect-video rounded-xl border bg-card shadow-sm"
      style={style}
    />
  )
}
