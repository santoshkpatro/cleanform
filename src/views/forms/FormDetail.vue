<script setup>
import { reactive, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getFormDetails } from '../../api'
import { Bar, Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const form = ref({})
const route = useRoute()
const router = useRouter()

const chartData = reactive({
  labels: ['January', 'February', 'March'],
  datasets: [
    { 
      data: [40, 20, 12] 
    }
  ],
})

const chartOptions = reactive({
  responsive: true,
})

onMounted(async () => {
  const { form_id } = route.params
  try {
    const { data } = await getFormDetails(form_id)
    form.value = data
  } catch (e) {
    console.log(e)
  }
})
</script>

<template>
  <div class="container">
    <div class="card" v-if="form">
      <div class="card-body">
        <div class="row">
          <div class="col-8">
            <h5>Name: {{ form.title }}</h5>
            <button
              @click="
                router.push({
                  name: 'builder',
                  params: { formId: form.id },
                })
              "
              class="btn btn-sm btn-primary"
            >
              Build the form
            </button>
          </div>
          <div class="col-4">
            <button
              class="btn btn-sm btn-secondary"
              @click="
                router.push({ name: 'formView', params: { slug: form.slug } })
              "
            >
              View link
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    <h5>Analytics</h5>
    <!-- <Bar :chart-options="chartOptions" :chart-data="chartData" /> -->
  </div>
</template>
