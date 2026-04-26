'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { chapters } from 'velite-data'
import { 
  Layers, Cpu, Hash, Grid, Binary, Zap, Waves, 
  Dice5, BarChart3, Radio, TrendingUp, BrainCircuit, 
  Target, Network, CheckCircle2, BookOpen
} from 'lucide-react'

const subjectIcons: Record<string, React.ReactNode> = {
  'foundations': <Layers className="w-4 h-4" />,
  'discrete-math': <Hash className="w-4 h-4" />,
  'linear-algebra': <Grid className="w-4 h-4" />,
  'numerical-methods': <Binary className="w-4 h-4" />,
  'calculus': <Zap className="w-4 h-4" />,
  'differential-equations': <Waves className="w-4 h-4" />,
  'probability': <Dice5 className="w-4 h-4" />,
  'statistics': <BarChart3 className="w-4 h-4" />,
  'information-theory': <Radio className="w-4 h-4" />,
  'optimization': <TrendingUp className="w-4 h-4" />,
  'ml-architect': <BrainCircuit className="w-4 h-4" />,
  'reinforcement-learning': <Target className="w-4 h-4" />,
  'graph-ml': <Network className="w-4 h-4" />,
  'conclusion': <CheckCircle2 className="w-4 h-4" />,
}

interface SidebarContentProps {
  pathname: string
  openSubjects: string[]
  setOpenSubjects: (value: string[]) => void
}

export function SidebarContent({ pathname, openSubjects, setOpenSubjects }: SidebarContentProps) {
  // Group chapters by subject and sort them by 'order'
  const subjectsMap = chapters.reduce((acc, chapter) => {
    const subject = chapter.subject
    if (!acc[subject]) {
      acc[subject] = []
    }
    acc[subject].push(chapter)
    return acc
  }, {} as Record<string, typeof chapters>)

  // Sort chapters within each subject
  Object.values(subjectsMap).forEach(group => {
    group.sort((a, b) => (a.order ?? 999) - (b.order ?? 999))
  })

  // Sort subjects by their pedagogical index
  const sortedSubjects = Object.keys(subjectsMap).sort((a, b) => {
    const aIndex = subjectsMap[a][0]?.subjectIndex ?? 999
    const bIndex = subjectsMap[b][0]?.subjectIndex ?? 999
    return aIndex - bIndex
  })

  return (
    <Accordion 
      multiple 
      value={openSubjects} 
      onValueChange={setOpenSubjects} 
      className="w-full space-y-2"
    >
      {sortedSubjects.map((subject) => (
        <AccordionItem key={subject} value={subject} className="border-none">
          <AccordionTrigger className="flex items-center gap-3 py-3 px-4 rounded-xl hover:no-underline hover:bg-accent/50 transition-all text-sm font-bold group [&[data-state=open]>svg:last-child]:rotate-90">
            <div className="flex items-center gap-3 text-muted-foreground group-hover:text-primary transition-colors uppercase tracking-tight text-[11px]">
              <div className="p-1.5 rounded-lg bg-muted group-hover:bg-primary/10 group-hover:text-primary transition-colors">
                {subjectIcons[subject] || <BookOpen className="w-4 h-4" />}
              </div>
              {subject.replace(/-/g, ' ')}
            </div>
          </AccordionTrigger>
          <AccordionContent className="pt-1 pb-2">
            <ul className="space-y-1.5 ml-8 border-l border-border/50 pl-4">
              {subjectsMap[subject].map((chapter) => (
                <li key={chapter.permalink}>
                  <Link
                    href={chapter.permalink}
                    className={cn(
                      'block py-1.5 text-xs transition-all hover:text-primary relative group',
                      pathname === chapter.permalink 
                        ? 'font-bold text-primary translate-x-1' 
                        : 'text-muted-foreground hover:translate-x-1'
                    )}
                  >
                    {pathname === chapter.permalink && (
                      <span className="absolute -left-4 top-1/2 -translate-y-1/2 w-1 h-1 rounded-full bg-primary" />
                    )}
                    {chapter.title}
                  </Link>
                </li>
              ))}
            </ul>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  )
}

export function Sidebar() {
  const pathname = usePathname()

  // Group chapters by subject for sorting
  const subjectsMap = chapters.reduce((acc, chapter) => {
    const subject = chapter.subject
    if (!acc[subject]) acc[subject] = []
    acc[subject].push(chapter)
    return acc
  }, {} as Record<string, typeof chapters>)

  const sortedSubjects = Object.keys(subjectsMap).sort((a, b) => {
    const aIndex = subjectsMap[a][0]?.subjectIndex ?? 999
    const bIndex = subjectsMap[b][0]?.subjectIndex ?? 999
    return aIndex - bIndex
  })

  const currentSubject = chapters.find(c => c.permalink === pathname)?.subject || sortedSubjects[0]
  
  const [openSubjects, setOpenSubjects] = React.useState<string[]>([currentSubject])

  const lastPathname = React.useRef(pathname)

  React.useEffect(() => {
    if (currentSubject && pathname !== lastPathname.current) {
      setOpenSubjects(prev => Array.from(new Set([...prev, currentSubject])))
      lastPathname.current = pathname
    }
  }, [currentSubject, pathname])

  return (
    <aside className="hidden lg:block w-80 border-r h-[calc(100vh-4rem)] sticky top-16 overflow-y-auto bg-background/50 backdrop-blur-sm">
      <ScrollArea className="h-full py-8 px-6">
        <div className="mb-6 px-4">
          <h2 className="text-[10px] font-black uppercase tracking-[0.2em] text-muted-foreground/50">
            Course Curriculum
          </h2>
        </div>
        <SidebarContent 
          pathname={pathname}
          openSubjects={openSubjects}
          setOpenSubjects={setOpenSubjects}
        />
      </ScrollArea>
    </aside>
  )
}
