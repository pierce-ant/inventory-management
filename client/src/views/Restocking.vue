<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <!-- Budget slider card -->
      <div class="card budget-card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.budgetTitle') }}</h3>
        </div>
        <div class="budget-body">
          <div class="budget-slider-row">
            <!--
              Slider range: $0–$100,000 in $1,000 steps.
              v-model.number ensures the ref stays a number (not a string).
              Changing this value triggers the watch below, rebuilding rows
              with a fresh greedy preselection — manual qty/checkbox edits reset.
            -->
            <input
              type="range"
              class="budget-slider"
              v-model.number="budget"
              min="0"
              max="100000"
              step="1000"
            />
            <span class="budget-amount">{{ formatCurrency(budget, currentCurrency) }}</span>
          </div>
          <p class="budget-hint">{{ t('restocking.budgetHint') }}</p>
        </div>
      </div>

      <!-- Summary stat cards -->
      <div class="stats-grid">
        <div class="stat-card info">
          <div class="stat-label">{{ t('restocking.itemsNeedingRestock') }}</div>
          <div class="stat-value">{{ rows.length }}</div>
        </div>
        <div class="stat-card success">
          <div class="stat-label">{{ t('restocking.selectedItems') }}</div>
          <div class="stat-value">{{ selectedRows.length }}</div>
        </div>
        <div class="stat-card warning">
          <div class="stat-label">{{ t('restocking.selectedCost') }}</div>
          <div class="stat-value stat-currency">{{ formatCurrency(selectedCost, currentCurrency) }}</div>
        </div>
        <div :class="['stat-card', budgetRemaining < 0 ? 'danger' : 'success']">
          <div class="stat-label">{{ t('restocking.budgetRemaining') }}</div>
          <div class="stat-value stat-currency">{{ formatCurrency(budgetRemaining, currentCurrency) }}</div>
        </div>
      </div>

      <!-- Inline success card shown after a restock order is placed -->
      <div v-if="placedOrder" class="card order-success-card">
        <div class="order-success-header">
          <strong>{{ t('restocking.orderPlaced') }}</strong>
        </div>
        <dl class="order-success-details">
          <div class="order-success-row">
            <dt>{{ t('orders.table.orderNumber') }}</dt>
            <dd>{{ placedOrder.order_number }}</dd>
          </div>
          <div class="order-success-row">
            <dt>{{ t('orders.table.totalCost') }}</dt>
            <dd>{{ formatCurrency(placedOrder.total_cost, currentCurrency) }}</dd>
          </div>
          <div class="order-success-row">
            <dt>{{ t('restocking.leadTime') }}</dt>
            <dd>{{ t('restocking.leadTimeDays', { days: placedOrder.lead_time_days }) }}</dd>
          </div>
          <div class="order-success-row">
            <dt>{{ t('restocking.expectedDelivery') }}</dt>
            <dd>{{ formatDate(placedOrder.expected_delivery) }}</dd>
          </div>
        </dl>
        <button class="btn-secondary" @click="navigate('/orders')">
          {{ t('restocking.viewInOrders') }}
        </button>
      </div>

      <!-- All items adequately stocked — no rows to show -->
      <div v-if="rows.length === 0" class="card">
        <p class="empty-state">{{ t('restocking.noRecommendations') }}</p>
      </div>

      <!-- Recommendations table -->
      <div v-else class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendations') }}</h3>
        </div>

        <!--
          Shown when rows exist but greedy preselection picked nothing
          because every item's line cost exceeds the available budget.
        -->
        <p v-if="selectedRows.length === 0" class="budget-too-low">
          {{ t('restocking.budgetTooLow') }}
        </p>

        <div class="table-container">
          <table class="restock-table">
            <thead>
              <tr>
                <th class="col-include">{{ t('restocking.table.include') }}</th>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.itemName') }}</th>
                <th>{{ t('restocking.table.category') }}</th>
                <th>{{ t('restocking.table.warehouse') }}</th>
                <th>{{ t('restocking.table.onHand') }}</th>
                <th>{{ t('restocking.table.reorderPoint') }}</th>
                <th>{{ t('restocking.table.forecastedDemand') }}</th>
                <th>{{ t('restocking.table.trend') }}</th>
                <th class="col-qty">{{ t('restocking.table.qtyToOrder') }}</th>
                <th>{{ t('restocking.table.unitCost') }}</th>
                <th>{{ t('restocking.table.lineCost') }}</th>
                <th>{{ t('restocking.table.leadTime') }}</th>
              </tr>
            </thead>
            <tbody>
              <!--
                Key on sku — each inventory item appears at most once since we
                deduplicate during the join. Index as key would cause incorrect
                DOM reuse when rows reorder after a budget change.
              -->
              <tr v-for="row in rows" :key="row.sku">
                <td class="col-include">
                  <input type="checkbox" v-model="row.selected" />
                </td>
                <td><strong>{{ row.sku }}</strong></td>
                <td>{{ row.name }}</td>
                <td>{{ row.category }}</td>
                <td>{{ row.warehouse }}</td>
                <td>{{ row.quantity_on_hand }}</td>
                <td>{{ row.reorder_point }}</td>
                <td>{{ row.forecasted_demand }}</td>
                <td>
                  <span :class="['badge', row.trend]">{{ t(`trends.${row.trend}`) }}</span>
                </td>
                <td class="col-qty">
                  <!-- Only editable when the row is included in the order -->
                  <input
                    v-if="row.selected"
                    type="number"
                    class="qty-input"
                    v-model.number="row.qty"
                    min="1"
                  />
                  <span v-else class="qty-text">{{ row.qty }}</span>
                </td>
                <td>{{ formatCurrency(row.unit_cost, currentCurrency) }}</td>
                <td><strong>{{ formatCurrency(row.qty * row.unit_cost, currentCurrency) }}</strong></td>
                <td>{{ t('restocking.leadTimeDays', { days: row.lead_time_days }) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Place Order action row -->
        <div class="order-actions">
          <p v-if="isOverBudget" class="over-budget-warning">{{ t('restocking.overBudget') }}</p>
          <button
            class="btn-primary-order"
            :disabled="submitting || selectedRows.length === 0 || isOverBudget || selectedRows.some(r => !(r.qty > 0))"
            @click="placeOrder"
          >
            {{ submitting ? t('restocking.placingOrder') : t('restocking.placeOrder') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import { useRouter } from '../composables/useRouter'
import { formatCurrency } from '../utils/currency'

// Trend weight constants for urgency scoring.
// "increasing" items are twice as urgent as "stable" and 4x "decreasing".
const TREND_WEIGHTS = { increasing: 2, stable: 1, decreasing: 0.5 }

export default {
  name: 'Restocking',
  setup() {
    const { t, currentCurrency, currentLocale } = useI18n()
    const { selectedLocation, selectedCategory, getCurrentFilters } = useFilters()
    const { navigate } = useRouter()

    const loading = ref(true)
    const error = ref(null)
    const submitting = ref(false)

    // Holds the last successfully placed order; drives the inline success card.
    const placedOrder = ref(null)

    // Raw API data — mutations trigger recomputation of sortedCandidates.
    const forecasts = ref([])
    const inventoryItems = ref([])

    // USD budget. Displayed via formatCurrency so JPY users see the converted value.
    const budget = ref(25000)

    /**
     * Sorted restock candidates, computed from raw API data.
     *
     * Step 1 — Join: match each demand forecast to its inventory record by SKU.
     *   Forecasts with no inventory entry are skipped (can't compute stock gap).
     *
     * Step 2 — Filter: compute
     *   recommendedQty = max(forecasted_demand, reorder_point) − quantity_on_hand
     *   Skip items where this is ≤ 0 (stock already covers the forecast).
     *
     * Step 3 — Sort: urgencyScore = recommendedQty × trend weight.
     *   Descending urgency; tie-break alphabetically by SKU for determinism.
     *
     * NOTE: budget-dependent selection is NOT done here; that lives in the
     * watch below so it can react to budget changes independently of the data.
     */
    const sortedCandidates = computed(() => {
      // O(1) inventory lookup by SKU
      const inventoryBySku = new Map(
        inventoryItems.value.map(item => [item.sku, item])
      )

      const candidates = []

      for (const forecast of forecasts.value) {
        const inv = inventoryBySku.get(forecast.item_sku)
        if (!inv) continue // no matching inventory record — skip

        const recommendedQty =
          Math.max(forecast.forecasted_demand, inv.reorder_point) - inv.quantity_on_hand
        if (recommendedQty <= 0) continue // item is adequately stocked — skip

        const weight = TREND_WEIGHTS[forecast.trend] ?? 1
        const urgencyScore = recommendedQty * weight

        candidates.push({
          sku: inv.sku,
          name: inv.name,
          category: inv.category,
          warehouse: inv.warehouse,
          quantity_on_hand: inv.quantity_on_hand,
          reorder_point: inv.reorder_point,
          forecasted_demand: forecast.forecasted_demand,
          trend: forecast.trend,
          recommendedQty,
          urgencyScore,
          unit_cost: inv.unit_cost,
          // lead_time_days is new on inventory items; default to 0 if absent
          lead_time_days: inv.lead_time_days ?? 0
        })
      }

      // Sort most-urgent first; break ties by SKU so ordering is stable
      candidates.sort((a, b) => {
        if (b.urgencyScore !== a.urgencyScore) return b.urgencyScore - a.urgencyScore
        return a.sku.localeCompare(b.sku)
      })

      return candidates
    })

    /**
     * Mutable rows ref — rebuilt whenever sortedCandidates or budget changes.
     *
     * Greedy preselection: walk the sorted list and select a row if its full
     * recommended-qty cost fits in the remaining budget.  We deliberately keep
     * walking after a row that doesn't fit so cheaper items further down can
     * still be included (knapsack greedy, not earliest-exit).
     *
     * Each row carries user-editable `selected` and `qty` fields.  Because
     * rows is a ref containing reactive objects, v-model bindings in the
     * template mutate these fields reactively.  Manual edits intentionally
     * reset when the budget slider moves or new data loads (accepted UX).
     */
    const rows = ref([])

    watch(
      [sortedCandidates, budget],
      ([newCandidates, newBudget]) => {
        let remaining = newBudget

        rows.value = newCandidates.map(c => {
          const lineCost = c.recommendedQty * c.unit_cost
          let selected = false

          if (lineCost <= remaining) {
            selected = true
            remaining -= lineCost
          }
          // Whether or not this row fits, continue checking cheaper rows below

          return {
            ...c,
            qty: c.recommendedQty, // user-editable; reset on every rebuild
            selected
          }
        })
      },
      { immediate: true } // run synchronously on first render so rows is populated
    )

    // Derived state — reactive because they depend on the mutable rows ref
    const selectedRows = computed(() => rows.value.filter(r => r.selected))

    const selectedCost = computed(() =>
      selectedRows.value.reduce((sum, r) => sum + r.qty * r.unit_cost, 0)
    )

    const budgetRemaining = computed(() => budget.value - selectedCost.value)

    const isOverBudget = computed(() => budgetRemaining.value < 0)

    const loadData = async () => {
      try {
        loading.value = true
        error.value = null
        const filters = getCurrentFilters()

        // Period and status filters are intentionally ignored here:
        // inventory has no time dimension and restock logic is status-agnostic.
        const [forecastsData, inventoryData] = await Promise.all([
          api.getDemandForecasts(),
          api.getInventory({ warehouse: filters.warehouse, category: filters.category })
        ])

        forecasts.value = forecastsData
        inventoryItems.value = inventoryData
      } catch (err) {
        error.value = 'Failed to load data: ' + err.message
      } finally {
        loading.value = false
      }
    }

    // Reload when warehouse or category filter changes
    watch([selectedLocation, selectedCategory], () => {
      loadData()
    })

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return dateString
      const locale = currentLocale.value === 'ja' ? 'ja-JP' : 'en-US'
      return date.toLocaleDateString(locale, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const placeOrder = async () => {
      if (submitting.value || selectedRows.value.length === 0 || isOverBudget.value) return

      submitting.value = true
      error.value = null

      try {
        const order = await api.createRestockOrder({
          budget: budget.value,
          items: selectedRows.value.map(r => ({ sku: r.sku, quantity: r.qty }))
        })

        placedOrder.value = order

        // Reload so recommendations reflect newly ordered quantities
        await loadData()
      } catch (err) {
        error.value = 'Failed to place order: ' + err.message
      } finally {
        submitting.value = false
      }
    }

    onMounted(loadData)

    return {
      t,
      currentCurrency,
      navigate,
      loading,
      error,
      submitting,
      placedOrder,
      budget,
      rows,
      selectedRows,
      selectedCost,
      budgetRemaining,
      isOverBudget,
      formatCurrency,
      formatDate,
      placeOrder
    }
  }
}
</script>

<style scoped>
/* Budget card body */
.budget-body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.budget-slider-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.budget-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  min-width: 130px;
  flex-shrink: 0;
}

.budget-hint {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

/*
 * Custom range slider — no existing slider component in this app.
 * Track: design-system slate (#e2e8f0). Thumb: primary blue (#2563eb).
 * Both -webkit- and -moz- prefixes required for cross-browser coverage.
 */
.budget-slider {
  -webkit-appearance: none;
  appearance: none;
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: #e2e8f0;
  outline: none;
  cursor: pointer;
}

.budget-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #2563eb;
  border: 2px solid #ffffff;
  box-shadow: 0 0 0 2px #2563eb;
  cursor: pointer;
  transition: box-shadow 0.15s ease;
}

.budget-slider::-webkit-slider-thumb:hover {
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2);
}

.budget-slider::-moz-range-thumb {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #2563eb;
  border: 2px solid #ffffff;
  box-shadow: 0 0 0 2px #2563eb;
  cursor: pointer;
}

/* Currency values in stat cards use a smaller font so long strings fit */
.stat-currency {
  font-size: 1.5rem;
}

/* Order placed success card — green left border to signal success */
.order-success-card {
  border-left: 4px solid #059669;
}

.order-success-header {
  font-size: 1rem;
  color: #059669;
  margin-bottom: 1rem;
}

.order-success-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.625rem 2rem;
  margin-bottom: 1rem;
}

.order-success-row {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.order-success-row dt {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.order-success-row dd {
  font-size: 0.938rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

/* Empty state — no restock candidates */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #64748b;
  font-size: 0.938rem;
}

/* Hint shown when greedy selection produced zero selected rows */
.budget-too-low {
  font-size: 0.875rem;
  color: #92400e;
  background: #fef3c7;
  border: 1px solid #fcd34d;
  border-radius: 6px;
  padding: 0.625rem 0.875rem;
  margin-bottom: 1rem;
}

/* Table — allow horizontal scroll without wrapping cells */
.restock-table {
  white-space: nowrap;
}

.col-include {
  width: 64px;
  text-align: center;
}

.col-qty {
  width: 110px;
}

.qty-input {
  width: 80px;
  padding: 0.25rem 0.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  font-size: 0.875rem;
  font-family: inherit;
  color: #0f172a;
}

.qty-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
}

.qty-text {
  color: #64748b;
}

/* Action row below the table */
.order-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid #e2e8f0;
  flex-wrap: wrap;
}

.over-budget-warning {
  font-size: 0.875rem;
  color: #dc2626;
  font-weight: 500;
  margin: 0;
}

/*
 * Primary order button — styled after TasksModal's .task-add-btn:
 * purple gradient, white text, float-up hover, disabled opacity.
 */
.btn-primary-order {
  padding: 0.75rem 1.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  white-space: nowrap;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.btn-primary-order:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-primary-order:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Secondary button used on the success card */
.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-secondary:hover {
  background: #e2e8f0;
}
</style>
