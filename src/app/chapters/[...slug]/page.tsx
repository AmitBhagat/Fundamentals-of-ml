import { chapters } from 'velite-data'
import { notFound } from 'next/navigation'
import { Metadata } from 'next'
import Link from 'next/link'
import { Zap, Clock } from 'lucide-react'

interface PageProps {
  params: Promise<{ slug: string[] }>
}

export async function generateStaticParams() {
  return chapters.map((chapter) => ({
    slug: chapter.slug.split('/'),
  }))
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params
  const slugPath = slug.join('/')
  const chapter = chapters.find((c) => c.slug === slugPath)
  if (!chapter) return {}

  return {
    title: `${chapter.title} | Mathematics`,
    description: chapter.description,
  }
}

export default async function ChapterPage({ params }: PageProps) {
  const { slug } = await params
  const slugPath = slug.join('/')
  const chapter = chapters.find((c) => c.slug === slugPath)

  if (!chapter) {
    notFound()
  }

  // Process content for Callouts and Labs
  let processedContent = chapter.content
    // Transform Blockquotes with [!TYPE] into themed callouts
    .replace(/<blockquote>\s*<p>\s*\[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]\s*(?:<\/p>)?/gi, (match, type) => {
      return `<blockquote data-type="${type.toLowerCase()}">`
    })
    // Wrap details/summary content properly if needed
    .replace(/<details>(.*?)<\/details>/gs, (match, inner) => {
      const summaryMatch = inner.match(/<summary>(.*?)<\/summary>/)
      const summary = summaryMatch ? summaryMatch[0] : '<summary>Reveal Intuition</summary>'
      const rest = inner.replace(summary, '').trim()
      return `<details>${summary}<div>${rest}</div></details>`
    })
    // Placeholder for Lab shortcodes
    .replace(/\[LAB:(.*?)\]/g, (match, labId) => {
      return `<div class="my-10 p-8 rounded-3xl bg-primary/5 border-2 border-dashed border-primary/20 flex flex-col items-center justify-center text-center gap-4">
        <div class="bg-primary text-primary-foreground p-3 rounded-full"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-flask-conical"><path d="M10 2v8L4.36 20.5a2 2 0 0 0 1.7 2.95h11.88a2 2 0 0 0 1.7-2.95L14 10V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/></svg></div>
        <div class="space-y-1">
          <div class="font-bold">Interactive Lab: ${labId.replace(/_/g, ' ')}</div>
          <div class="text-sm text-muted-foreground italic">Visualizer loading... (Placeholder)</div>
        </div>
      </div>`
    })

  return (
    <article className="prose prose-slate dark:prose-invert max-w-none">
      {chapter.description && (
        <header className="mb-12 not-prose space-y-6">
          
          <div className="flex flex-wrap gap-4 items-center text-sm font-medium">
            {chapter.complexity && (
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary border border-primary/20 capitalize">
                <Zap className="w-3.5 h-3.5" /> {chapter.complexity}
              </div>
            )}
            {chapter.estimated_time && (
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-muted text-muted-foreground border border-border">
                <Clock className="w-3.5 h-3.5" /> {chapter.estimated_time}
              </div>
            )}
          </div>

          <div className="h-1 w-20 bg-primary/20 rounded" />
        </header>
      )}
      <div dangerouslySetInnerHTML={{ __html: processedContent }} />

      <div className="mt-16 pt-8 border-t flex flex-col sm:flex-row items-center justify-between gap-4 not-prose">
        {(() => {
          // Sort chapters by pedagogical order first
          const sortedChapters = [...chapters].sort((a, b) => {
            if (a.subjectIndex !== b.subjectIndex) {
              return (a.subjectIndex ?? 999) - (b.subjectIndex ?? 999)
            }
            return (a.order ?? 999) - (b.order ?? 999)
          })

          const currentIndex = sortedChapters.findIndex(c => c.slug === slugPath)
          const prev = sortedChapters[currentIndex - 1]
          const next = sortedChapters[currentIndex + 1]

          return (
            <>
              {prev ? (
                <Link 
                  href={prev.permalink}
                  className="flex flex-col gap-1 items-start group w-full sm:max-w-[45%]"
                >
                  <span className="text-xs text-muted-foreground font-medium uppercase tracking-wider">Previous</span>
                  <span className="text-sm font-semibold group-hover:text-primary transition-colors text-balance">
                    ← {prev.title}
                  </span>
                </Link>
              ) : <div />}

              {next ? (
                <Link 
                  href={next.permalink}
                  className="flex flex-col gap-1 items-end group text-right w-full sm:max-w-[45%]"
                >
                  <span className="text-xs text-muted-foreground font-medium uppercase tracking-wider">Next</span>
                  <span className="text-sm font-semibold group-hover:text-primary transition-colors text-balance">
                    {next.title} →
                  </span>
                </Link>
              ) : <div />}
            </>
          )
        })()}
      </div>
    </article>
  )
}
