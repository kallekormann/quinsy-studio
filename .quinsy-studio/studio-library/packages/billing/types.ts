export type BillingProviderId = 'stripe' | 'lemon-squeezy';

export interface CheckoutSession {
  url: string;
  id: string;
}

export interface BillingProvider {
  id: BillingProviderId;
  /** `userId` is the Payload user id; webhooks use it to find the subscriber. */
  createCheckout(planId: string, customerEmail: string, userId?: string): Promise<CheckoutSession>;
  handleWebhook(payload: unknown, signature: string): Promise<void>;
}
