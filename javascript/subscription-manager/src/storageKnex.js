import { Client as ClientDC, Subscription as SubDC } from './models.js';

export class SQLBackend {
  /**
   * @param {object} knexConfig — e.g. { client:'pg', connection: 'postgres://…' }
   */
  constructor(knexConfig) {
    this.knex = require('knex')(knexConfig);
  }

  async init() {
    // Run once at startup
    await this.knex.schema.hasTable('clients').then(exists => {
      if (!exists) {
        return this.knex.schema.createTable('clients', tbl => {
          tbl.string('id').primary();
          tbl.string('email').unique().notNullable();
          tbl.string('phone');
          tbl.string('fingerprint');
          tbl.timestamp('created_at').defaultTo(this.knex.fn.now());
        });
      }
    });
    await this.knex.schema.hasTable('subscriptions').then(exists => {
      if (!exists) {
        return this.knex.schema.createTable('subscriptions', tbl => {
          tbl.increments('id').primary();
          tbl.string('client_id').references('id').inTable('clients');
          tbl.string('plan_key').notNullable();
          tbl.timestamp('start_date').notNullable();
          tbl.timestamp('end_date').notNullable();
          tbl.boolean('active').defaultTo(true);
        });
      }
    });
  }

  async getClientByEmail(email) {
    const row = await this.knex('clients').where({ email }).first();
    if (!row) return null;
    return new ClientDC(row);
  }

  async addClient(client) {
    await this.knex('clients').insert({
      id: client.id,
      email: client.email,
      phone: client.phone,
      fingerprint: client.fingerprint,
      created_at: client.createdAt,
    });
  }

  async getSubscriptions(clientId) {
    const rows = await this.knex('subscriptions').where({ client_id: clientId });
    return rows.map(r => new SubDC({
      clientId: r.client_id,
      planKey: r.plan_key,
      startDate: r.start_date,
      endDate: r.end_date,
      active: r.active
    }));
  }

  async addSubscription(sub) {
    await this.knex('subscriptions').insert({
      client_id: sub.clientId,
      plan_key: sub.planKey,
      start_date: sub.startDate,
      end_date: sub.endDate,
      active: sub.active
    });
  }
}
