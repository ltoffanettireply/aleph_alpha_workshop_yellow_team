<script lang="ts" setup>
import UsecaseQaAnswerActions from './UsecaseQaAnswerActions.vue'
import SkeletonPlaceholderContainer from '@/@core/components/SkeletonPlaceholderContainer.vue'
import { UsecaseQaAnswerStatus, type UsecaseQaChatEntry } from '@/models/UsecaseQaChatEntry'
import { AaText } from '@aleph-alpha/ds-components-vue'

defineProps<{
  chatEntry: UsecaseQaChatEntry
}>()
</script>

<template>
  <div class="w-179 p-M gap-XS text-core-content-primary flex grow rounded">
    <div
      class="border-core-border-default flex size-8 flex-shrink-0 items-center justify-center rounded-full border"
    >
      <span class="i-aa-logo flex size-4 flex-shrink-0" />
    </div>
    <SkeletonPlaceholderContainer
      v-if="chatEntry.answer.status === UsecaseQaAnswerStatus.PENDING"
      :bar-count="4"
      :bar-height-px="32"
      class="gap-y-lg"
    />
    <div v-else class="flex w-full flex-col justify-center">
      <!-- SQL Query -->
      <AaText element="div" class="whitespace-pre-line">
        <div v-if="chatEntry.answer.answer">
          <h3 class="text-lg font-semibold mb-2">SQL Query:</h3>
          <pre class="bg-gray-100 p-2 rounded mb-4 overflow-x-auto">{{ chatEntry.answer.answer }}</pre>
        </div>
        <div v-else>No answer found</div>
      </AaText>

      <!-- Query Error -->
      <AaText v-if="chatEntry.answer.query_error" element="div" class="mt-4 text-red-600 whitespace-pre-line">
        <h3 class="text-lg font-semibold mb-2">Error:</h3>
        <pre class="bg-red-50 p-2 rounded">{{ chatEntry.answer.query_error }}</pre>
      </AaText>

      <!-- Query Results -->
      <div v-if="chatEntry.answer.query_results" class="mt-4">
        <h3 class="text-lg font-semibold mb-2">Query Results:</h3>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  v-for="(header, index) in chatEntry.answer.query_results.headers"
                  :key="index"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(row, rowIndex) in chatEntry.answer.query_results.rows" :key="rowIndex">
                <td
                  v-for="(cell, cellIndex) in row"
                  :key="cellIndex"
                  class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                >
                  {{ cell }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="pt-L text-core-content-tertiary flex items-center justify-between">
        <UsecaseQaAnswerActions :chat-entry="chatEntry" />
      </div>
    </div>
  </div>
</template>
