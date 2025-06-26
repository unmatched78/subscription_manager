import { TrialAlreadyUsed, PlanNotFound } from './exceptions.js';
import { Subscription } from './models.js';

export class SubscriptionService {
  /**
   * @param {*} storage  — any backend implementing the 4 async methods
   * @param {{[key:string]:Plan}} plans
   * @param {() => string} idGenerator
   */
  constructor(storage, plans, idGenerator) {
    this.storage = storage;
    this.plans = plans;
    this.idGenerator = idGenerator;
  }

  async registerClient(email, phone = null, fingerprint = null) {
    let client = await this.storage.getClientByEmail(email);
    if (client) return client;

    client = { id: this.idGenerator(), email, phone, fingerprint, createdAt: new Date() };
    await this.storage.addClient(client);
    return client;
  }

  async startSubscription(client, planKey) {
    const plan = this.plans[planKey];
    if (!plan) throw new PlanNotFound(`No such plan: ${planKey}`);

    if (planKey === 'free_trial') {
      const subs = await this.storage.getSubscriptions(client.id);
      if (subs.some(s => s.planKey === 'free_trial')) {
        throw new TrialAlreadyUsed('Free trial already used');
      }
    }

    const now = new Date();
    const endDate = new Date(now.getTime() + plan.durationDays * 24*60*60*1000);
    const sub = new Subscription({
      clientId: client.id,
      planKey,
      startDate: now,
      endDate,
      active: true
    });
    await this.storage.addSubscription(sub);
    return sub;
  }

  async renewSubscription(client, planKey) {
    return this.startSubscription(client, planKey);
  }

  async cancelSubscription(client, planKey) {
    const subs = await this.storage.getSubscriptions(client.id);
    subs.filter(s => s.planKey === planKey && s.active)
        .forEach(s => { s.active = false; });
    // Note: persistent update would require extra storage method
  }

  async isActive(client, planKey) {
    const now = new Date();
    const subs = await this.storage.getSubscriptions(client.id);
    return subs.some(s =>
      s.planKey === planKey &&
      s.active &&
      s.startDate <= now && now < s.endDate
    );
  }
}
