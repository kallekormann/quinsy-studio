import type { BillingProvider } from '../types';

export const stripeProvider: BillingProvider = {
  id: 'stripe',
  async createCheckout(planId, customerEmail) {
    return {
      id: `cs_stub_${planId}`,
      url: `https://checkout.stripe.com/stub?plan=${planId}&email=${encodeURIComponent(customerEmail)}`,
    };
  },
  async handleWebhook() {
    throw new Error('Implement Stripe webhook verification in project');
  },
};
