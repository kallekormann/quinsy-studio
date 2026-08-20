export type BillingProviderId = 'stripe' | 'lemon-squeezy';

export interface CheckoutSession {
  url: string;
  id: string;
}

export interface BillingProvider {
  id: BillingProviderId;
  createCheckout(planId: string, customerEmail: string): Promise<CheckoutSession>;
  handleWebhook(payload: unknown, signature: string): Promise<void>;
}
