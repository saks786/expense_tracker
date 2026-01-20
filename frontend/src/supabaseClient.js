/**
 * Supabase Client Configuration
 * Handles Supabase connection, authentication, and real-time features
 */
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Supabase configuration missing! Check your .env file.')
}

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  },
  realtime: {
    params: {
      eventsPerSecond: 10
    }
  }
})

// Export auth helpers
export const supabaseAuth = supabase.auth

/**
 * Subscribe to real-time changes for a table
 * @param {string} table - Table name
 * @param {function} callback - Callback function for changes
 * @returns {object} Subscription object
 */
export function subscribeToTable(table, callback) {
  return supabase
    .channel(`public:${table}`)
    .on('postgres_changes', { event: '*', schema: 'public', table }, callback)
    .subscribe()
}

/**
 * Unsubscribe from real-time channel
 * @param {object} subscription - Subscription object
 */
export function unsubscribeFrom(subscription) {
  if (subscription) {
    supabase.removeChannel(subscription)
  }
}

console.log('✅ Supabase client initialized:', supabaseUrl)
