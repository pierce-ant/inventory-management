import { ref } from 'vue'

// Shared router state (singleton pattern)
const currentPath = ref(window.location.pathname)

window.addEventListener('popstate', () => {
  currentPath.value = window.location.pathname
})

export function useRouter() {
  const navigate = (path) => {
    if (path !== currentPath.value) {
      window.history.pushState({}, '', path)
      currentPath.value = path
    }
  }

  return { currentPath, navigate }
}
