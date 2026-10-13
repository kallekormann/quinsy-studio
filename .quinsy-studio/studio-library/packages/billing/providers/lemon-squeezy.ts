import { createHmac, timingSafeEqual } from 'node:crypto'

import type { BillingProvider } from '../types'

function required(name: string): string {
  const value = process.env[name]
  if (!value) {
    throw new Error(`Missing ${name}`)
  }
  return value
}

export const lemonSqueezyProvider: BillingProvider = {
  id: 'lemon-squeezy',
  async createCheckout(planId, customerEmail, userId) {
    const response = await fetch('https://api.lemonsqueezy.com/v1/checkouts', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${required('LEMONSQUEEZY_API_KEY')}`,
        Accept: 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json',
      },
      body: JSON.stringify({
        data: {
          type: 'checkouts',
          attributes: {
            checkout_data: {
              email: customerEmail,
              ...(userId ? { custom: { user_id: userId } } : {}),
            },
          },
          relationships: {
            store: { data: { type: 'stores', id: required('LEMONSQUEEZY_STORE_ID') } },
            variant: { data: { type: 'variants', id: planId } },
          },
        },
      }),
    })
    if (!response.ok) {
      throw new Error(`Lemon Squeezy checkout failed (${response.status})`)
    }
    const session = (await response.json()) as { data: { id: string; attributes: { url: string } } }
    return { id: session.data.id, url: session.data.attributes.url }
  },
  async handleWebhook(payload, signature) {
    const raw = typeof payload === 'string' ? payload : ''
    if (!raw) {
      throw new Error('Lemon Squeezy webhook needs the raw body string')
    }
    const expected = createHmac('sha256', required('LEMONSQUEEZY_WEBHOOK_SECRET')).update(raw).digest('hex')
    const a = Buffer.from(expected)
    const b = Buffer.from(signature)
    if (a.length !== b.length || !timingSafeEqual(a, b)) {
      throw new Error('Lemon Squeezy webhook signature mismatch')
    }
  },
}
