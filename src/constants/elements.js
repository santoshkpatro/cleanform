export const elements = [
  {
    id: 1,
    name: 'Input Field',
    description: 'Basic input field',
    defaultValues: {
      label: 'New Input Field',
      description: '',
      is_required: false,
      type: 'input_field',
      properties: {
        type: 'text',
        placeholder: '',
      },
      layouts: {},
      validations: {}
    },
  },
  {
    id: 2,
    name: 'Radio Field',
    description: 'Basic radio field',
    defaultValues: {
      label: 'New Radio Field',
      description: '',
      is_required: false,
      type: 'radio_field',
      properties: {
        options: ['Option 1', 'Option 2', 'Option 3'],
        default_option: 'Option 2',
      },
      layouts: {},
      validations: {}
    },
  },
  {
    id: 3,
    name: 'Checkbox Field',
    description: 'Checkbox field',
    defaultValues: {
      label: 'New Checkbox Field',
      description: '',
      is_required: false,
      type: 'checkbox_field',
      properties: {
        choices: [
          'Choice 1',
          'Choice 2',
          'Choice 3',
          'Choice 4',
          'Choice 5',
          'Choice 6',
        ],
        default_checked_choices: ['Choice 3', 'Choice 4'],
      },
      layouts: {},
      validations: {}
    },
  },
]
