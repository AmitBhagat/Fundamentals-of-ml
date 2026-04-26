'use client'

import React from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { CommandPalette } from '@/components/command-palette'
import { ModeToggle } from '@/components/mode-toggle'
import { Menu } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { chapters } from 'velite-data'
import { usePathname } from 'next/navigation'
import { SidebarContent } from './sidebar'

export function Navbar() {
  const pathname = usePathname()
  const [isOpen, setIsOpen] = React.useState(false)
  
  // Sorting logic for default open subject
  const subjectsMap = chapters.reduce((acc, chapter) => {
    const subject = chapter.subject
    if (!acc[subject]) acc[subject] = []
    acc[subject].push(chapter)
    return acc
  }, {} as Record<string, typeof chapters>)

  const sortedSubjects = Object.keys(subjectsMap)
    .filter(subject => subject !== 'conclusion')
    .sort((a, b) => {
      const aIndex = subjectsMap[a][0]?.subjectIndex ?? 999
      const bIndex = subjectsMap[b][0]?.subjectIndex ?? 999
      return aIndex - bIndex
    })

  const currentSubject = chapters.find(c => c.permalink === pathname)?.subject || sortedSubjects[0]
  const [openSubjects, setOpenSubjects] = React.useState<string[]>([currentSubject])

  // Sync open subject when pathname changes
  React.useEffect(() => {
    if (currentSubject) {
      setOpenSubjects(prev => Array.from(new Set([...prev, currentSubject])))
    }
  }, [currentSubject])
  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center gap-4 px-4 md:px-8">
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
          <SheetTrigger
            render={
              <Button variant="ghost" size="icon" className="lg:hidden">
                <Menu className="h-5 w-5" />
              </Button>
            }
          />
          <SheetContent side="left" className="w-[300px] sm:w-[400px] p-0 border-r-0">
            <div className="flex flex-col h-full bg-background/95 backdrop-blur-xl">
              <div className="p-6 border-b">
                <Link href="/" onClick={() => setIsOpen(false)} className="flex items-center gap-2 font-bold text-xl tracking-tight">
                  <div className="bg-primary text-primary-foreground p-1 rounded-md">∑</div>
                  <span>Mathematics</span>
                </Link>
              </div>
              <ScrollArea className="flex-1 px-4 py-6">
                <SidebarContent 
                  pathname={pathname}
                  openSubjects={openSubjects}
                  setOpenSubjects={setOpenSubjects}
                />
              </ScrollArea>
              <div className="p-6 border-t bg-muted/30">
                <div className="flex items-center justify-between">
                  <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-widest">
                    Version 1.0.4
                  </p>
                  <ModeToggle />
                </div>
              </div>
            </div>
          </SheetContent>
        </Sheet>
        
        <Link href="/" className="flex items-center gap-2 font-bold text-xl tracking-tight">
          <motion.div 
            initial={{ rotate: -10, scale: 0.9 }}
            animate={{ rotate: 0, scale: 1 }}
            className="bg-primary text-primary-foreground p-1 rounded-md"
          >
            ∑
          </motion.div>
          <span>Mathematics</span>
        </Link>

        <div className="flex flex-1 items-center justify-end gap-2">
          <div className="hidden md:flex">
            <CommandPalette />
          </div>
          <ModeToggle />
        </div>
      </div>
    </nav>
  )
}
