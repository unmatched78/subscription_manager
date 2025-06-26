import { Client, Subscription } from './models.js';

export class InMemoryBackend {
  constructor() {
    this.clients = new Map();            // email → Client
    this.subscriptions = new Map();      // clientId → [Subscription]
  }

  async getClientByEmail(email) {
    return this.clients.get(email) || null;
  }

  async addClient(client) {
    this.clients.set(client.email, client);
  }

  async getSubscriptions(clientId) {
    return this.subscriptions.get(clientId) || [];
  }

  async addSubscription(sub) {
    const arr = this.subscriptions.get(sub.clientId) || [];
    arr.push(sub);
    this.subscriptions.set(sub.clientId, arr);
  }
}
