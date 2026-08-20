import type { BillingProvider } from '../types';

export const lemonSqueezyProvider: BillingProvider = {
  id: 'lemon-squeezy',
  async createCheckout(planId, customerEmail) {
    return {
      id: `ls_stub_${planId}`,
      url: `https://checkout.lemonsqueezy.com/stub?plan=${planId}&email=${encodeURIComponent(customerEmail)}`,
    };
  },
  async handleWebhook() {
    throw new Error('Implement Lemon Squeezy webhook verification in project');
  },
};
