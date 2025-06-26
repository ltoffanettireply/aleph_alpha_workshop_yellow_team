import { z } from 'zod'

export interface CustomRagRequest {
  question: string
}

const QueryResultsSchema = z.object({
  headers: z.array(z.string()),
  rows: z.array(z.array(z.any()))
})

export const CUSTOM_RAG_RESPONSE_SCHEMA = z.object({
  answer: z.string().optional(),
  query_results: QueryResultsSchema.optional(),
  query_error: z.string().optional(),
})

export type CustomRagResponse = z.infer<typeof CUSTOM_RAG_RESPONSE_SCHEMA>
export type QueryResults = z.infer<typeof QueryResultsSchema>
