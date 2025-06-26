export class Client {
  constructor({ id, email, phone = null, fingerprint = null, createdAt = new Date() }) {
    this.id = id;
    this.email = email;
    this.phone = phone;
    this.fingerprint = fingerprint;
    this.createdAt = createdAt;
  }
}

export class Plan {
  constructor(key, name, priceCents, durationDays, category) {
    this.key = key;
    this.name = name;
    this.priceCents = priceCents;
    this.durationDays = durationDays;
    this.category = category;
  }
}

export class Subscription {
  constructor({ clientId, planKey, startDate = new Date(), endDate, active = true }) {
    this.clientId = clientId;
    this.planKey = planKey;
    this.startDate = startDate;
    this.endDate = endDate;
    this.active = active;
  }
}
