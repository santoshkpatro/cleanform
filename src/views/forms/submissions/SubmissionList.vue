<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { HotTable } from '@handsontable/vue3'
import { registerAllModules } from 'handsontable/registry'
import { getSubmissions } from '../../../api'
import { concat, uniq } from 'lodash'

const route = useRoute()
const router = useRouter()

// register Handsontable's modules
registerAllModules()

const submissions = ref([])

async function fetchSubmissions() {
  const { form_id } = route.params

  try {
    const res = await getSubmissions(form_id)
    if (res.status !== 200) throw new Error('Something went wrong')

    submissions.value = []
    const { data } = res

    // refactoring data
    let columns = []
    data.results.forEach((result) => {
      columns = concat(columns, Object.keys(result.data))
    })

    columns = uniq(columns)
    submissions.value.push(columns)

    data.results.forEach((result) => {
      const row = []

      columns.forEach((column) => {
        if (result.data.hasOwnProperty(column)) {
          row.push(result.data[column])
        } else {
          row.push('')
        }
      })

      submissions.value.push(row)
    })
  } catch (e) {
    console.log(e)
  }
}

onMounted(() => {
  fetchSubmissions()
})

function handleRefresh() {
  fetchSubmissions()
}
</script>

<template>
  <div class="container">
    <div class="my-3">
      <h3>
        Submissions
        <button class="btn btn-sm btn-secondary" @click="handleRefresh">
          Refresh
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-arrow-clockwise"
            viewBox="0 0 16 16"
          >
            <path
              fill-rule="evenodd"
              d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"
            />
            <path
              d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"
            />
          </svg>
        </button>
      </h3>
      <hot-table
        v-if="submissions.length"
        :data="submissions"
        :rowHeaders="true"
        :colHeaders="true"
        licenseKey="non-commercial-and-evaluation"
      ></hot-table>
    </div>
  </div>
</template>

<style></style>
