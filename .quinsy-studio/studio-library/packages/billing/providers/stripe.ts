import { createHmac, timingSafeEqual } from 'node:crypto'

import type { BillingProvider } from '../types'

function required(name: string): string {
  const value = process.env[name]
  if (!value) {
    throw new Error(`Missing ${name}`)
  }
  return value
}

const SIGNATURE_TOLERANCE_SECONDS = 300

export const stripeProvider: BillingProvider = {
  id: 'stripe',
  async createCheckout(planId, customerEmail, userId) {
    const body = new URLSearchParams({
      mode: 'subscription',
      customer_email: customerEmail,
      'line_items[0][price]': planId,
      'line_items[0][quantity]': '1',
      success_url: required('STRIPE_SUCCESS_URL'),
      cancel_url: required('STRIPE_CANCEL_URL'),
    })
    if (userId) {
      body.set('client_reference_id', userId)
      body.set('metadata[user_id]', userId)
      body.set('subscription_data[metadata][user_id]', userId)
    }
    const response = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${required('STRIPE_SECRET_KEY')}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body,
    })
    if (!response.ok) {
      throw new Error(`Stripe checkout failed (${response.status})`)
    }
    const session = (await response.json()) as { id: string; url: string }
    return { id: session.id, url: session.url }
  },
  async handleWebhook(payload, signature) {
    const raw = typeof payload === 'string' ? payload : ''
    if (!raw) {
      throw new Error('Stripe webhook needs the raw body string')
    }
    let timestamp = ''
    const candidates: string[] = []
    for (const part of signature.split(',')) {
      const [key, value = ''] = part.trim().split('=')
      if (key === 't') timestamp = value
      if (key === 'v1') candidates.push(value)
    }
    const sentAt = Number(timestamp)
    if (!timestamp || !Number.isFinite(sentAt)) {
      throw new Error('Stripe webhook signature has no timestamp')
    }
    if (Math.abs(Date.now() / 1000 - sentAt) > SIGNATURE_TOLERANCE_SECONDS) {
      throw new Error('Stripe webhook timestamp outside tolerance (possible replay)')
    }
    const expected = Buffer.from(
      createHmac('sha256', required('STRIPE_WEBHOOK_SECRET')).update(`${timestamp}.${raw}`).digest('hex'),
    )
    const matches = candidates.some((given) => {
      const b = Buffer.from(given)
      return b.length === expected.length && timingSafeEqual(expected, b)
    })
    if (!matches) {
      throw new Error('Stripe webhook signature mismatch')
    }
  },
}
