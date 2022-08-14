<script setup>
import { reactive, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getForms, createForm, updateForm, deleteForm } from '../../api'

const router = useRouter()
const forms = ref([])
const newForm = reactive({
  title: '',
  description: '',
  is_live: false,
})

onMounted(async () => {
  try {
    const { data } = await getForms()
    forms.value = data.results
  } catch (e) {
    console.log(e)
  }
})

async function handleUpdateForm(form) {
  try {
    const { data } = await updateForm(form.id, form)
    console.log(data)
  } catch (e) {
    console.log(e)
  } finally {
  }
}

async function createNewForm() {
  try {
    const { data } = await createForm(newForm)
    forms.value.push(data)
  } catch (e) {
    console.log(e)
  } finally {
    newForm.title = ''
    newForm.description = ''
  }
}

async function handleDeleteForm(form){
  try {
    await deleteForm(form.id)

    forms.value = forms.value.filter(f => f.id !== form.id)
  } catch (e) {
    console.log(e)
  }
}
</script>

<template>
  <div class="container">
    <!-- Create a new form -->
    <form @submit.prevent="createNewForm" class="mb-5">
      <div class="mb-2">
        <label for="title" class="form-label">Form name</label>
        <input
          type="text"
          class="form-control"
          v-model="newForm.title"
          required
        />
      </div>
      <div class="mb-2">
        <label for="title" class="form-label">Description</label>
        <textarea
          class="form-control"
          id="exampleFormControlTextarea1"
          rows="3"
          v-model="newForm.description"
        ></textarea>
      </div>
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-sm btn-success">
          Create form
        </button>
      </div>
    </form>

    <!-- Existing forms -->
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Name</th>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col">Is Live</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(form, index) in forms" :key="form.id">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ form.title }}</td>
          <td>
            <button
              class="btn btn-sm btn-primary"
              @click="
                router.push({
                  name: 'formDetail',
                  params: { form_id: form.id },
                })
              "
            >
              View Detail
            </button>
          </td>
          <td>
            <button
              class="btn btn-sm btn-primary"
              @click="
                router.push({
                  name: 'formSubmissions',
                  params: { form_id: form.id },
                })
              "
            >
              View Submissions
            </button>
          </td>
          <td>
            <div class="form-check form-switch">
              <input
                v-model="form.is_live"
                class="form-check-input"
                type="checkbox"
                role="switch"
                id="flexSwitchCheckChecked"
                :checked="form.is_live"
                @input="handleUpdateForm({ ...form, is_live: !form.is_live })"
              />
            </div>
          </td>
          <td>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-trash3"
              viewBox="0 0 16 16"
              @click="handleDeleteForm(form)"
            >
              <path
                d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z"
              />
            </svg>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
