import Link from "next/link";
import { chapters } from "velite-data";
import { ArrowRight, BookOpen, Calculator, Cpu, ChevronRight, Zap, Layers, Network, Database, Sigma } from "lucide-react";
import { motion } from "framer-motion";

const subjectIcons: Record<string, any> = {
  'foundations': Database,
  'linear-algebra': Layers,
  'calculus': Sigma,
  'probability': Zap,
  'statistics': Network,
  'optimization': Cpu,
  'information-theory': BookOpen,
  'numerical-methods': Calculator,
}

export default function Home() {
  // Group chapters by subject
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

  const firstChapter = chapters[0]?.permalink || '#'

  return (
    <div className="space-y-24 py-10">
      {/* Hero Section */}
      <section className="space-y-6 text-center lg:text-left max-w-3xl">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-widest mb-4">
          <Zap className="w-3 h-3" /> 2026 Edition
        </div>
        <h1 className="text-6xl font-black tracking-tighter font-heading leading-tight">
          Master the Math Behind <span className="text-primary">Intelligence.</span>
        </h1>
        <p className="text-xl text-muted-foreground leading-relaxed">
          A high-performance, interactive curriculum designed for the next generation of AI engineers. 
          Built for clarity, speed, and mathematical rigor.
        </p>
        <div className="flex flex-wrap gap-4 pt-4 justify-center lg:justify-start">
          <Link 
            href={firstChapter}
            className="h-14 px-8 rounded-full bg-primary text-primary-foreground font-bold flex items-center gap-2 hover:opacity-90 transition-all shadow-xl shadow-primary/20"
          >
            Start Learning <ArrowRight className="w-4 h-4" />
          </Link>
          <Link 
            href="/chapters/linear-algebra/linear-algebra"
            className="h-14 px-8 rounded-full border border-border font-bold flex items-center gap-2 hover:bg-accent transition-all"
          >
            Explore Curriculum
          </Link>
        </div>
      </section>

      {/* Subject Grid */}
      <section className="space-y-12">
        <div className="flex flex-col gap-2">
          <h2 className="text-3xl font-black tracking-tight font-heading">Curriculum Path</h2>
          <p className="text-muted-foreground">11 core subjects, 105 chapters, 1 path to mastery.</p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          {sortedSubjects.map((subject) => {
            const subjectChapters = subjectsMap[subject]
            const Icon = subjectIcons[subject] || BookOpen
            const firstSubChapter = subjectChapters[0]?.permalink || '#'

            return (
              <Link 
                key={subject} 
                href={firstSubChapter}
                className="group p-8 border rounded-3xl bg-card hover:bg-accent/30 transition-all border-border/50 hover:border-primary/50 relative overflow-hidden"
              >
                <div className="relative z-10 space-y-6">
                  <div className="bg-primary/5 p-4 rounded-2xl w-fit group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-500">
                    <Icon className="w-8 h-8" />
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-2xl font-black font-heading capitalize">
                      {subject.replace(/-/g, ' ')}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {subjectChapters.length} Chapters · {subjectChapters[0]?.order}-{subjectChapters[subjectChapters.length-1]?.order}
                    </p>
                  </div>
                  <div className="flex items-center gap-1 text-primary font-bold text-sm">
                    View Subject <ChevronRight className="w-4 h-4" />
                  </div>
                </div>
                {/* Subtle Background Accent */}
                <div className="absolute -right-4 -bottom-4 opacity-5 group-hover:opacity-10 transition-opacity">
                   <Icon className="w-32 h-32" />
                </div>
              </Link>
            )
          })}
        </div>
      </section>

      {/* Features */}
      <section className="grid gap-12 md:grid-cols-3 border-t border-border/50 pt-24 pb-12">
        <div className="space-y-4">
          <div className="bg-primary/5 p-3 rounded-xl w-fit">
            <Calculator className="w-6 h-6 text-primary" />
          </div>
          <h4 className="font-black text-xl font-heading">Zero-Compromise Math</h4>
          <p className="text-muted-foreground leading-relaxed">KaTeX rendered equations with zero layout shift. Perfect clarity for every derivation.</p>
        </div>
        <div className="space-y-4">
          <div className="bg-primary/5 p-3 rounded-xl w-fit">
            <Cpu className="w-6 h-6 text-primary" />
          </div>
          <h4 className="font-black text-xl font-heading">Applied Intuition</h4>
          <p className="text-muted-foreground leading-relaxed">We skip the academic fluff. Every concept is tied back to actual training dynamics and loss surfaces.</p>
        </div>
        <div className="space-y-4">
          <div className="bg-primary/5 p-3 rounded-xl w-fit">
            <BookOpen className="w-6 h-6 text-primary" />
          </div>
          <h4 className="font-black text-xl font-heading">Interactive Labs</h4>
          <p className="text-muted-foreground leading-relaxed">Don't just read about gradients. Visualize them in real-time with our built-in laboratories.</p>
        </div>
      </section>
    </div>
  );
}
