import { defineConfig, s } from 'velite'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import remarkGfm from 'remark-gfm'

export default defineConfig({
  root: 'content',
  output: {
    data: '.velite',
    assets: 'public/static',
    base: '/static/',
    name: '[name]-[hash:8].[ext]',
    clean: true
  },
  collections: {
    chapters: {
      name: 'Chapter',
      pattern: '**/*.md',
      schema: s
        .object({
          title: s.string().optional(),
          description: s.string().max(999).optional(),
          complexity: s.string().optional(),
          estimated_time: s.string().optional(),
          prerequisites: s.array(s.string()).optional(),
          date: s.isodate().optional(),
          content: s.markdown()
        })
        .transform((data, { meta }) => {
          const normalizedPath = meta.path.replace(/\\/g, '/')
          const relativePath = normalizedPath.split('content/').pop() || normalizedPath
          const cleanPath = relativePath.replace(/\.[^/.]+$/, '')
          const subject = cleanPath.split('/')[0]

          // Extract chapter number from content or title (e.g., "# Chapter 21: SVD" -> 21)
          const chapterNumberMatch = data.content.match(/Chapter (\d+)/i)
          const order = chapterNumberMatch ? parseInt(chapterNumberMatch[1], 10) : 999

          const SUBJECT_ORDER = [
            'foundations',
            'discrete-math',
            'linear-algebra',
            'numerical-methods',
            'calculus',
            'differential-equations',
            'probability',
            'statistics',
            'information-theory',
            'optimization',
            'ml-architect',
            'reinforcement-learning',
            'graph-ml',
            'conclusion'
          ]
          const subjectOrder = SUBJECT_ORDER.indexOf(subject)
          const subjectIndex = subjectOrder === -1 ? 999 : subjectOrder

          const slug = cleanPath.replace(/\/index$/, '')
          return { 
            ...data, 
            title: data.title || (meta.basename ?? '').replace(/_/g, ' ').replace(/\.[^/.]+$/, '').replace(/\b\w/g, l => l.toUpperCase()),
            slug,
            permalink: `/chapters/${slug}`,
            subject,
            order,
            subjectIndex
          }
        })
    }
  },
  // Ensure math is rendered for both markdown and mdx
  markdown: {
    remarkPlugins: [remarkMath, remarkGfm],
    rehypePlugins: [rehypeKatex]
  },
  mdx: {
    remarkPlugins: [remarkMath, remarkGfm],
    rehypePlugins: [rehypeKatex]
  }
})
