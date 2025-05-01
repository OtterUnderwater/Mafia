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
          accent: '#A41817',
          text: '#F2EFE6',
          tooltip: '#99948E',
          error: '#ED8B10',
          success: '#09D8C6',
          info: '#09D8C6',
          warning: '#ED8B10',
        },
      },
      light: {
        colors: {
          primary: '#5F0E0D',
          secondary: '#A41817',
          background: '#07070B',
          accent: '#A41817',
          text: '#F2EFE6',
          tooltip: '#99948E',
          error: '#ED8B10',
          success: '#09D8C6',
          info: '#09D8C6',
          warning: '#ED8B10',
        },
      },
    },
  },
})

