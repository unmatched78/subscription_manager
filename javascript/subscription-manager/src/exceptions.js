export class SubscriptionError extends Error {}
export class TrialAlreadyUsed extends SubscriptionError {}
export class PlanNotFound extends SubscriptionError {}
export class NotFoundError extends SubscriptionError {}
