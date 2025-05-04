// Purpose: Tailwind CSS configuration for custom styling
module.exports = {
    content: [
      './src/ui/**/*.py',
    ],
    theme: {
      extend: {
        colors: {
          primary: '#0D1B2A',
          accent: '#FF6B6B',
        },
      },
    },
    plugins: [],
  };