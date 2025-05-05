// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        colors: {
          primary: '#5F0E0D',
          secondary: '#A41817',
          background: '#07070B',
          accent: '#F42C1D',
          text: '#F2EFE6',
          tooltip: '#99948E',
          error: '#F42D1D',
          success: '#16BB33',
          info: '#09D8C6',
          warning: '#F4841D',
        },
      },
      light: {
        colors: {
          primary: '#5F0E0D',
          secondary: '#A41817',
          background: '#07070B',
          accent: '#F42C1D',
          text: '#F2EFE6',
          tooltip: '#99948E',
          error: '#F42D1D',
          success: '#16BB33',
          info: '#09D8C6',
          warning: '#F4841D',
        },
      },
    },
  },
})

