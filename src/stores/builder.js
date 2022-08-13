import { defineStore } from 'pinia'

export const useBuilderStore = defineStore({
    id: 'builder',
    state: () => ({
        form: {},
        formElements: [],
        selectedElement: null
    }),
    getters: {
        ordering: (state) => state.formElements.map((element) => element.id)
    },
    actions: {
        setForm(form_data) {
            this.form = form_data
        },
        setFormElements(elements) {
            this.formElements = elements
        },
        setSelectedElement(element) {
            this.selectedElement = element
        },
        removeSelectedElement() {
            this.selectedElement = null
        },
        addNewElement(newElement) {
            this.formElements.push(newElement)
            this.form.elements.push(newElement.id)
        },
        deleteFormElement(element) {
            this.formElements = this.formElements.filter(e => e.id !== element.id)
            this.form.elements = this.formElements.map(e => e.id)
        } 
    }
})