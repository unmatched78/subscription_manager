import { SubscriptionService, SQLBackend, Plan } from 'subscription-manager';
import { v4 as uuidv4 } from 'uuid';

const db = new SQLBackend({
  client: 'pg',
  connection: 'postgres://user:pass@localhost/db'
});

const plans = {
  free_trial: new Plan('free_trial', '14-day Trial', 0, 14, 'Trial'),
  basic:      new Plan('basic',      'Basic Plan',    999, 30, 'Paid')
};

const svc = new SubscriptionService(db, plans, uuidv4);

(async () => {
  const client = await svc.registerClient('alice@example.com', '+250780000000', 'fingerprint123');
  const trial  = await svc.startSubscription(client, 'free_trial');
  console.log(`Expires: ${trial.endDate}`);
})();
