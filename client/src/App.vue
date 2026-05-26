<template>
  <div class="app">
    <aside :class="['sidebar', { collapsed: sidebarCollapsed }]">
      <div class="sidebar-brand">
        <span class="sidebar-title">{{ t('nav.companyName') }}</span>
        <span class="sidebar-subtitle">{{ t('nav.subtitle') }}</span>
      </div>
      <nav class="sidebar-nav">
        <a
          href="/"
          :class="{ active: currentPath === '/' }"
          @click.exact.prevent="navigate('/')"
          :title="t('nav.overview')"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
          </svg>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </a>
        <a
          href="/inventory"
          :class="{ active: currentPath === '/inventory' }"
          @click.exact.prevent="navigate('/inventory')"
          :title="t('nav.inventory')"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
            <line x1="12" y1="22.08" x2="12" y2="12"/>
          </svg>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </a>
        <a
          href="/orders"
          :class="{ active: currentPath === '/orders' }"
          @click.exact.prevent="navigate('/orders')"
          :title="t('nav.orders')"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
            <rect x="9" y="3" width="6" height="4" rx="1"/>
            <line x1="9" y1="12" x2="15" y2="12"/>
            <line x1="9" y1="16" x2="13" y2="16"/>
          </svg>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </a>
        <a
          href="/spending"
          :class="{ active: currentPath === '/spending' }"
          @click.exact.prevent="navigate('/spending')"
          :title="t('nav.finance')"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"/>
            <line x1="12" y1="20" x2="12" y2="4"/>
            <line x1="6" y1="20" x2="6" y2="14"/>
            <line x1="2" y1="20" x2="22" y2="20"/>
          </svg>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </a>
        <a
          href="/demand"
          :class="{ active: currentPath === '/demand' }"
          @click.exact.prevent="navigate('/demand')"
          :title="t('nav.demandForecast')"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
            <polyline points="17 6 23 6 23 12"/>
          </svg>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </a>
        <a
          href="/restocking"
          :class="{ active: currentPath === '/restocking' }"
          @click.exact.prevent="navigate('/restocking')"
          :title="t('nav.restocking')"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="1 4 1 10 7 10"/>
            <polyline points="23 20 23 14 17 14"/>
            <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/>
          </svg>
          <span class="nav-label">{{ t('nav.restocking') }}</span>
        </a>
        <a
          href="/reports"
          :class="{ active: currentPath === '/reports' }"
          @click.exact.prevent="navigate('/reports')"
          :title="t('nav.reports')"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="12" width="4" height="9"/>
            <rect x="10" y="7" width="4" height="14"/>
            <rect x="17" y="3" width="4" height="18"/>
          </svg>
          <span class="nav-label">{{ t('nav.reports') }}</span>
        </a>
      </nav>

      <div class="sidebar-toggle-wrap">
        <button
          class="sidebar-toggle"
          @click="toggleSidebar"
          :title="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        >
          <svg v-if="!sidebarCollapsed" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="11 17 6 12 11 7"/>
            <polyline points="18 17 13 12 18 7"/>
          </svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="13 17 18 12 13 7"/>
            <polyline points="6 17 11 12 6 7"/>
          </svg>
          <span class="nav-label">Collapse</span>
        </button>
      </div>
    </aside>

    <div :class="['app-body', { 'sidebar-collapsed': sidebarCollapsed }]">
      <header class="top-bar">
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </header>
      <FilterBar />
      <main class="main-content">
        <component :is="currentView" />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import { useRouter } from './composables/useRouter'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import Dashboard from './views/Dashboard.vue'
import Inventory from './views/Inventory.vue'
import Orders from './views/Orders.vue'
import Demand from './views/Demand.vue'
import Spending from './views/Spending.vue'
import Reports from './views/Reports.vue'
import Restocking from './views/Restocking.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher,
    Dashboard,
    Inventory,
    Orders,
    Demand,
    Spending,
    Reports,
    Restocking
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const { currentPath, navigate } = useRouter()

    const sidebarCollapsed = ref(localStorage.getItem('sidebarCollapsed') === 'true')
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      localStorage.setItem('sidebarCollapsed', String(sidebarCollapsed.value))
    }

    const routes = {
      '/': Dashboard,
      '/inventory': Inventory,
      '/orders': Orders,
      '/demand': Demand,
      '/spending': Spending,
      '/restocking': Restocking,
      '/reports': Reports
    }

    const currentView = computed(() => routes[currentPath.value] || Dashboard)
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(loadTasks)

    return {
      t,
      sidebarCollapsed,
      toggleSidebar,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask,
      currentPath,
      navigate,
      currentView
    }
  }
}
</script>

<style>
:root {
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.5rem;
  --space-6: 2rem;
  --space-8: 3rem;
  --radius-sm: 6px;
  --radius-md: 10px;
  --shadow-card: 0 1px 2px rgba(15, 23, 42, 0.05);
  --shadow-raised: 0 4px 12px rgba(15, 23, 42, 0.08);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f8fafc;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  min-height: 100vh;
}

/* ── Sidebar ──────────────────────────────────────────── */

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 240px;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  padding: var(--space-4) var(--space-3);
  z-index: 200;
  transition: width 0.2s ease;
  overflow: hidden;
}

.sidebar-brand {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-3) var(--space-3) var(--space-5);
}

.sidebar-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: -0.015em;
}

.sidebar-subtitle {
  font-size: 0.75rem;
  color: #64748b;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.55rem var(--space-3);
  border-radius: var(--radius-sm);
  color: #94a3b8;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 2px;
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
}

.sidebar-nav a:hover {
  background: rgba(148, 163, 184, 0.1);
  color: #e2e8f0;
}

.sidebar-nav a.active {
  background: rgba(59, 130, 246, 0.15);
  color: #ffffff;
  box-shadow: inset 3px 0 0 #3b82f6;
}

.sidebar-nav a svg {
  flex-shrink: 0;
}

/* ── Sidebar toggle button ────────────────────────────── */

.sidebar-toggle-wrap {
  margin-top: auto;
  border-top: 1px solid rgba(148, 163, 184, 0.15);
  padding-top: var(--space-3);
}

.sidebar-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.55rem var(--space-3);
  border-radius: var(--radius-sm);
  color: #94a3b8;
  font-size: 0.875rem;
  font-weight: 500;
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s, color 0.15s;
}

.sidebar-toggle:hover {
  background: rgba(148, 163, 184, 0.1);
  color: #e2e8f0;
}

.sidebar-toggle svg {
  flex-shrink: 0;
}

/* ── Sidebar collapsed state (JS-controlled) ──────────── */

.sidebar.collapsed {
  width: 64px;
  padding: var(--space-4) var(--space-2);
}

.sidebar.collapsed .sidebar-brand {
  padding: var(--space-3) 0 var(--space-5);
  align-items: center;
}

.sidebar.collapsed .sidebar-title,
.sidebar.collapsed .sidebar-subtitle {
  display: none;
}

.sidebar.collapsed .sidebar-nav a {
  justify-content: center;
  padding: 0.55rem;
  gap: 0;
}

.sidebar.collapsed .sidebar-toggle {
  justify-content: center;
  padding: 0.55rem;
  gap: 0;
}

.sidebar.collapsed .nav-label {
  display: none;
}

/* ── App body (right column) ──────────────────────────── */

.app-body {
  margin-left: 240px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.2s ease;
}

.app-body.sidebar-collapsed {
  margin-left: 64px;
}

/* ── Top bar ──────────────────────────────────────────── */

.top-bar {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: 0 var(--space-6);
  position: sticky;
  top: 0;
  z-index: 100;
}

/* ── Main content ─────────────────────────────────────── */

.main-content {
  flex: 1;
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
  padding: var(--space-6);
}

/* ── Responsive ───────────────────────────────────────── */

@media (max-width: 1024px) {
  .sidebar {
    width: 64px;
    padding: var(--space-4) var(--space-2);
  }

  .sidebar-brand {
    padding: var(--space-3) 0 var(--space-5);
    align-items: center;
  }

  .sidebar-title,
  .sidebar-subtitle {
    display: none;
  }

  .sidebar-nav a {
    justify-content: center;
    padding: 0.55rem;
    gap: 0;
  }

  .nav-label {
    display: none;
  }

  .app-body {
    margin-left: 64px;
  }
}

@media (max-width: 768px) {
  .top-bar {
    padding: 0 var(--space-4);
  }

  .main-content {
    padding: var(--space-4);
  }
}

/* ── Page header ──────────────────────────────────────── */

.page-header {
  margin-bottom: var(--space-5);
}

.page-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.25rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: #64748b;
  font-size: 0.9rem;
}

/* ── Stats grid ───────────────────────────────────────── */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}

/* ── Stat card ────────────────────────────────────────── */

.stat-card {
  background: white;
  padding: var(--space-5);
  border-radius: var(--radius-md);
  border: 1px solid #e2e8f0;
  box-shadow: var(--shadow-card);
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: #cbd5e1;
  box-shadow: var(--shadow-raised);
}

.stat-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: #ea580c;
}

.stat-card.success .stat-value {
  color: #059669;
}

.stat-card.danger .stat-value {
  color: #dc2626;
}

.stat-card.info .stat-value {
  color: #2563eb;
}

/* ── Card ─────────────────────────────────────────────── */

.card {
  background: white;
  border-radius: var(--radius-md);
  padding: var(--space-5);
  border: 1px solid #e2e8f0;
  box-shadow: var(--shadow-card);
  margin-bottom: var(--space-5);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
  letter-spacing: -0.015em;
}

/* ── Table ────────────────────────────────────────────── */

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

th {
  text-align: left;
  padding: var(--space-3) var(--space-4);
  font-weight: 600;
  color: #64748b;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: var(--space-3) var(--space-4);
  border-top: 1px solid #f1f5f9;
  color: #334155;
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: #f8fafc;
}

/* ── Badge ────────────────────────────────────────────── */

.badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: #d1fae5;
  color: #065f46;
}

.badge.warning {
  background: #fed7aa;
  color: #92400e;
}

.badge.danger {
  background: #fecaca;
  color: #991b1b;
}

.badge.info {
  background: #dbeafe;
  color: #1e40af;
}

.badge.increasing {
  background: #d1fae5;
  color: #065f46;
}

.badge.decreasing {
  background: #fecaca;
  color: #991b1b;
}

.badge.stable {
  background: #e0e7ff;
  color: #3730a3;
}

.badge.high {
  background: #fecaca;
  color: #991b1b;
}

.badge.medium {
  background: #fed7aa;
  color: #92400e;
}

.badge.low {
  background: #dbeafe;
  color: #1e40af;
}

/* ── Loading / Error ──────────────────────────────────── */

.loading {
  text-align: center;
  padding: var(--space-6);
  color: #64748b;
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  margin: var(--space-4) 0;
  font-size: 0.938rem;
}

/* ── Buttons ──────────────────────────────────────────── */

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #2563eb;
  color: #ffffff;
  border: none;
  height: 38px;
  padding: 0 var(--space-4);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
  text-decoration: none;
}

.btn-primary:hover {
  background: #1d4ed8;
}

.btn-primary:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  color: #334155;
  border: 1px solid #e2e8f0;
  height: 38px;
  padding: 0 var(--space-4);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
  text-decoration: none;
}

.btn-secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-secondary:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
</style>
